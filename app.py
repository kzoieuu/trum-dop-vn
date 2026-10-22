import os
import os
import json
from flask import (Flask, render_template, g, request,
                   redirect, url_for, session)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from database import init_db, get_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key')


# ── Tiện ích DB ────────────────────────────────────────────────────────────
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def query_db(sql, args=(), one=False):
    db = get_db()
    cur = db.execute(sql, args)
    rows = cur.fetchall()
    return (rows[0] if rows else None) if one else rows


def execute_db(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur.lastrowid


def get_current_user():
    """Trả về dict user đang đăng nhập, hoặc None."""
    user_id = session.get('user_id')
    if user_id:
        return query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)
    return None


# ── Context processor: đưa current_user vào mọi template ──────────────────
@app.context_processor
def inject_user():
    return {'current_user': get_current_user()}


# ══════════════════════════════════════════════════════════════════════════
# TRANG CHỦ (F5 — cá nhân hóa)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/')
def home():
    user = get_current_user()

    # Lọc theo gợi ý cá nhân nếu có tham số
    applied = request.args.getlist('hint')
    if applied:
        placeholders = ','.join('?' * len(applied))
        restaurants = query_db(
            f'SELECT * FROM restaurants WHERE food_type IN ({placeholders}) '
            f'ORDER BY rating DESC', applied
        )
    else:
        restaurants = query_db(
            'SELECT * FROM restaurants ORDER BY rating DESC, review_count DESC'
        )

    total = len(restaurants)

    # Sở thích đã lưu của user
    preferences = []
    if user:
        prefs_raw   = user['preferences'] or '[]'
        preferences = json.loads(prefs_raw)

    restaurants_json = json.dumps([dict(r) for r in restaurants], ensure_ascii=False)

    return render_template('home.html',
                           active_page='home',
                           restaurants=restaurants,
                           total=total,
                           preferences=preferences,
                           restaurants_json=restaurants_json)


# ══════════════════════════════════════════════════════════════════════════
# VÒNG QUAY & BẢN ĐỒ
# ══════════════════════════════════════════════════════════════════════════
@app.route('/spin')
def spin():
    restaurants = query_db('SELECT * FROM restaurants ORDER BY rating DESC')
    restaurants_json = json.dumps([dict(r) for r in restaurants], ensure_ascii=False)
    return render_template('spin.html', active_page='spin',
                           restaurants_json=restaurants_json)


@app.route('/map')
def food_map():
    restaurants = query_db('SELECT * FROM restaurants ORDER BY is_featured DESC, rating DESC')
    return render_template('food_map.html', active_page='map',
                           restaurants=restaurants)


# ══════════════════════════════════════════════════════════════════════════
# DANH SÁCH QUÁN (F4 + F1)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/restaurants')
def restaurants():
    food_types  = request.args.getlist('food_type')
    price_range = request.args.get('price_range', '')
    districts   = request.args.getlist('district')
    keyword     = request.args.get('q', '').strip()

    sql    = 'SELECT * FROM restaurants WHERE 1=1'
    params = []

    if keyword:
        sql += ' AND (name LIKE ? OR food_type LIKE ? OR address LIKE ?)'
        kw = f'%{keyword}%'
        params.extend([kw, kw, kw])

    if food_types:
        placeholders = ','.join('?' * len(food_types))
        sql += f' AND food_type IN ({placeholders})'
        params.extend(food_types)

    if price_range:
        sql += ' AND price_range = ?'
        params.append(price_range)

    if districts:
        placeholders = ','.join('?' * len(districts))
        sql += f' AND district IN ({placeholders})'
        params.extend(districts)

    sql += ' ORDER BY is_featured DESC, rating DESC'

    restaurant_list = query_db(sql, params)
    total = len(restaurant_list)

    all_food_types = [r['food_type'] for r in
                      query_db('SELECT DISTINCT food_type FROM restaurants ORDER BY food_type')]
    all_districts  = [r['district'] for r in
                      query_db('SELECT DISTINCT district FROM restaurants ORDER BY district')]

    return render_template('restaurants.html',
                           active_page='restaurants',
                           restaurants=restaurant_list,
                           total=total,
                           selected_food_types=food_types,
                           selected_price_range=price_range,
                           selected_districts=districts,
                           keyword=keyword,
                           all_food_types=all_food_types,
                           all_districts=all_districts)


# ══════════════════════════════════════════════════════════════════════════
# CHI TIẾT QUÁN (F6 + F2)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/restaurants/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurant_detail(restaurant_id):
    restaurant = query_db(
        'SELECT * FROM restaurants WHERE id = ?', [restaurant_id], one=True
    )
    if restaurant is None:
        return render_template('404.html'), 404

    menu_items = query_db(
        'SELECT * FROM menu_items WHERE restaurant_id = ? ORDER BY price',
        [restaurant_id]
    )

    review_success = False
    review_error   = None

    # POST: gửi đánh giá
    if request.method == 'POST':
        return redirect(url_for('add_review', restaurant_id=restaurant_id))

    # Lấy tham số sau khi gửi đánh giá
    review_success = request.args.get('review_ok') == '1'

    reviews = query_db(
        'SELECT * FROM reviews WHERE restaurant_id = ? ORDER BY created_at DESC',
        [restaurant_id]
    )

    # Tính điểm trung bình thật từ DB
    total_reviews = len(reviews)
    avg_rating    = (sum(r['rating'] for r in reviews) / total_reviews) if total_reviews else restaurant['rating']
    star_counts   = {s: sum(1 for r in reviews if r['rating'] == s) for s in range(1, 6)}

    return render_template('restaurant_detail.html',
                           active_page='restaurants',
                           restaurant=restaurant,
                           menu_items=menu_items,
                           reviews=reviews,
                           avg_rating=avg_rating,
                           total_reviews=total_reviews,
                           star_counts=star_counts,
                           review_success=review_success,
                           review_error=review_error)


@app.route('/restaurants/<int:restaurant_id>/review', methods=['POST'])
def add_review(restaurant_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    rating  = request.form.get('rating', '').strip()
    content = request.form.get('content', '').strip()

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id,
                                review_ok='0') + '#reviews')
    if not content:
        return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id,
                                review_ok='0') + '#reviews')

    execute_db(
        'INSERT INTO reviews (restaurant_id, user_id, username, rating, content) VALUES (?,?,?,?,?)',
        [restaurant_id, user['id'], user['username'], int(rating), content]
    )

    # Cập nhật lại điểm trung bình trong bảng restaurants
    reviews = query_db('SELECT rating FROM reviews WHERE restaurant_id = ?', [restaurant_id])
    if reviews:
        avg = sum(r['rating'] for r in reviews) / len(reviews)
        execute_db('UPDATE restaurants SET rating=?, review_count=? WHERE id=?',
                   [round(avg, 1), len(reviews), restaurant_id])

    return redirect(url_for('restaurant_detail', restaurant_id=restaurant_id,
                            review_ok='1') + '#reviews')


# ══════════════════════════════════════════════════════════════════════════
# ĐĂNG KÝ (F9)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Đã đăng nhập thì về trang chủ
    if get_current_user():
        return redirect(url_for('home'))

    if request.method == 'POST':
        username  = request.form.get('username', '').strip()
        email     = request.form.get('email', '').strip().lower()
        password  = request.form.get('password', '')
        password2 = request.form.get('password2', '')

        # Kiểm tra đầu vào
        error = None
        if not username or len(username) < 3:
            error = 'Tên người dùng phải có ít nhất 3 ký tự.'
        elif not email or '@' not in email:
            error = 'Email không hợp lệ.'
        elif len(password) < 6:
            error = 'Mật khẩu phải có ít nhất 6 ký tự.'
        elif password != password2:
            error = 'Mật khẩu xác nhận không khớp.'
        else:
            # Kiểm tra trùng username / email
            existing = query_db(
                'SELECT id FROM users WHERE username = ? OR email = ?',
                [username, email], one=True
            )
            if existing:
                error = 'Tên người dùng hoặc email đã được sử dụng.'

        if error:
            return render_template('auth.html', active_page='auth', mode='register',
                                   error=error,
                                   form_data={'username': username, 'email': email})

        # Lưu tài khoản — mật khẩu được băm
        pw_hash = generate_password_hash(password)
        execute_db(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            [username, email, pw_hash]
        )
        return render_template('auth.html', active_page='auth', mode='login',
                               success='Đăng ký thành công! Hãy đăng nhập để tiếp tục.')

    return render_template('auth.html', active_page='auth', mode='register')


# ══════════════════════════════════════════════════════════════════════════
# ĐĂNG NHẬP (F9)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_current_user():
        return redirect(url_for('home'))

    if request.method == 'POST':
        username_or_email = request.form.get('username', '').strip()
        password          = request.form.get('password', '')

        user = query_db(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            [username_or_email, username_or_email.lower()], one=True
        )

        if user is None or not check_password_hash(user['password_hash'], password):
            return render_template('auth.html', active_page='auth', mode='login',
                                   error='Tên đăng nhập hoặc mật khẩu không đúng.',
                                   form_data={'username': username_or_email})

        # Lưu session
        session.clear()
        session['user_id'] = user['id']
        return redirect(url_for('home'))

    return render_template('auth.html', active_page='auth', mode='login')


# ══════════════════════════════════════════════════════════════════════════
# ĐĂNG XUẤT (F9)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# ══════════════════════════════════════════════════════════════════════════
# HỒ SƠ CÁ NHÂN (F9)
# ══════════════════════════════════════════════════════════════════════════
@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    # Đọc sở thích đã lưu
    prefs_raw   = user['preferences'] or '[]'
    preferences = json.loads(prefs_raw)
    pref_saved  = request.args.get('saved') == '1'

    return render_template('profile.html', active_page='profile',
                           user=user,
                           preferences=preferences,
                           pref_saved=pref_saved)


@app.route('/profile/preferences', methods=['POST'])
def update_preferences():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    prefs = request.form.getlist('preferences')
    execute_db(
        'UPDATE users SET preferences = ? WHERE id = ?',
        [json.dumps(prefs, ensure_ascii=False), user['id']]
    )
    return redirect(url_for('profile', saved='1'))


# ══════════════════════════════════════════════════════════════════════════
# LIÊN HỆ
# ══════════════════════════════════════════════════════════════════════════
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    sent = False
    form = None
    if request.method == 'POST':
        form = {
            'name':    request.form.get('name', '').strip(),
            'email':   request.form.get('email', '').strip(),
            'subject': request.form.get('subject', ''),
            'message': request.form.get('message', '').strip(),
        }
        # Lưu vào DB để admin xem sau (tạo bảng nếu chưa có)
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS contact_messages
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT, email TEXT, subject TEXT, message TEXT,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        db.execute('INSERT INTO contact_messages (name,email,subject,message) VALUES (?,?,?,?)',
                   [form['name'], form['email'], form['subject'], form['message']])
        db.commit()
        sent = True
        form = None  # xóa form sau khi gửi
    return render_template('contact.html', active_page='contact', sent=sent, form=form)


# ── Xử lý lỗi 404 ─────────────────────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
else:
    # Chạy trên production server (gunicorn)
    init_db()
    # Nạp dữ liệu mẫu nếu chưa có
    from seed import seed
    from database import get_db
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM restaurants').fetchone()[0]
        if count == 0:
            seed()
    except Exception:
        seed()
