# Thiết kế tính năng: AI Tóm tắt đánh giá quán ăn

**Dự án:** Trùm Đớp VN  
**Tính năng:** AI tóm tắt điểm khen / điểm chê  
**Phiên bản:** 1.0  

---

## 1. Kiến trúc tổng thể

```
Trình duyệt (client)
    │  Bấm "Làm mới" hoặc vào trang lần đầu
    ▼
Flask route: GET /restaurants/<id>/summary
    │
    ├─► SQLite (bảng ai_summaries)
    │       Nếu có cache và review_count không đổi → trả về ngay
    │
    └─► OpenAI API (gpt-4o-mini)
            Nếu chưa có cache hoặc review_count thay đổi
            → gọi API → lưu vào SQLite → trả về
```

---

## 2. Thay đổi database

### Bảng mới: `ai_summaries`

```sql
CREATE TABLE IF NOT EXISTS ai_summaries (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id           INTEGER NOT NULL UNIQUE,
    pros                    TEXT,   -- JSON array: ["...", "..."]
    cons                    TEXT,   -- JSON array: ["...", "..."]
    review_count_at_summary INTEGER DEFAULT 0,
    created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
```

**Giải thích:**
- `pros` và `cons` lưu dưới dạng JSON string, ví dụ: `'["Nước dùng ngon", "Phục vụ nhanh"]'`
- `review_count_at_summary`: số lượng đánh giá tại thời điểm tóm tắt — dùng để kiểm tra xem có cần làm mới không

---

## 3. Backend — Flask

### 3.1 Cập nhật `database.py`
Thêm câu lệnh tạo bảng `ai_summaries` vào hàm `init_db()`.

### 3.2 Tạo file mới: `ai_summary.py`

```python
# ai_summary.py — logic gọi OpenAI và quản lý cache

import os, json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

PROMPT_TEMPLATE = """
Bạn là trợ lý phân tích đánh giá nhà hàng. Dưới đây là các đánh giá của khách hàng về quán "{name}":

{reviews}

Hãy tóm tắt ngắn gọn thành 2 mục:
- pros: danh sách 2-3 điểm khách hàng khen (mỗi điểm tối đa 15 từ)
- cons: danh sách 1-2 điểm khách hàng chê (mỗi điểm tối đa 15 từ, nếu không có thì để mảng rỗng)

Trả về JSON theo đúng format:
{"pros": ["...", "..."], "cons": ["...", "..."]}
Chỉ trả về JSON, không giải thích thêm.
"""

def get_or_create_summary(restaurant_id, restaurant_name, reviews, db):
    """
    Trả về dict {"pros": [...], "cons": [...]}
    Ưu tiên đọc từ cache SQLite, chỉ gọi API khi cần.
    """
    total = len(reviews)
    if total == 0:
        return None

    # Kiểm tra cache
    cached = db.execute(
        'SELECT * FROM ai_summaries WHERE restaurant_id = ?', [restaurant_id]
    ).fetchone()

    if cached and cached['review_count_at_summary'] == total:
        return {
            'pros': json.loads(cached['pros']),
            'cons': json.loads(cached['cons']),
            'from_cache': True
        }

    # Gọi OpenAI API
    review_text = '\n'.join([f'- {r["username"]}: {r["content"]}' for r in reviews])
    prompt = PROMPT_TEMPLATE.format(name=restaurant_name, reviews=review_text)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.3,
        max_tokens=300,
    )

    raw = response.choices[0].message.content.strip()
    data = json.loads(raw)

    # Lưu cache
    db.execute('''
        INSERT INTO ai_summaries (restaurant_id, pros, cons, review_count_at_summary)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(restaurant_id) DO UPDATE SET
            pros=excluded.pros, cons=excluded.cons,
            review_count_at_summary=excluded.review_count_at_summary,
            created_at=CURRENT_TIMESTAMP
    ''', [restaurant_id, json.dumps(data['pros'], ensure_ascii=False),
          json.dumps(data['cons'], ensure_ascii=False), total])
    db.commit()

    return {'pros': data['pros'], 'cons': data['cons'], 'from_cache': False}
```

### 3.3 Cập nhật `app.py`

Thêm route mới:

```python
@app.route('/restaurants/<int:restaurant_id>/summary')
def ai_summary(restaurant_id):
    """Trả về tóm tắt AI dạng JSON cho trang chi tiết gọi bằng fetch()."""
    restaurant = query_db('SELECT * FROM restaurants WHERE id=?', [restaurant_id], one=True)
    if not restaurant:
        return {'error': 'Không tìm thấy quán'}, 404

    reviews = query_db(
        'SELECT * FROM reviews WHERE restaurant_id=?', [restaurant_id]
    )
    if not reviews:
        return {'error': 'Chưa có đủ đánh giá'}, 200

    try:
        from ai_summary import get_or_create_summary
        db = get_db()
        result = get_or_create_summary(restaurant_id, restaurant['name'], reviews, db)
        return result
    except Exception as e:
        return {'error': str(e)}, 500
```

Thêm tham số `force=1` để làm mới:

```python
@app.route('/restaurants/<int:restaurant_id>/summary/refresh', methods=['POST'])
def ai_summary_refresh(restaurant_id):
    """Xóa cache và tạo tóm tắt mới."""
    db = get_db()
    db.execute('DELETE FROM ai_summaries WHERE restaurant_id=?', [restaurant_id])
    db.commit()
    return redirect(url_for('ai_summary', restaurant_id=restaurant_id))
```

---

## 4. Frontend — HTML/JS

### 4.1 Vị trí trong `restaurant_detail.html`

Thêm khung tóm tắt **ngay trên** phần đánh giá chi tiết:

```html
<!-- Khung AI tóm tắt -->
<div class="ai-summary-box" id="ai-summary-box">
    <div class="ai-summary-header">
        <span>🤖 Tóm tắt từ AI</span>
        <button class="btn-refresh-summary" id="refresh-summary-btn"
                title="Làm mới tóm tắt">🔄 Làm mới</button>
    </div>
    <div class="ai-summary-body" id="ai-summary-body">
        <p class="ai-loading">⏳ Đang phân tích đánh giá...</p>
    </div>
</div>
```

### 4.2 Logic JS (trong `extra_js` block)

```javascript
async function loadSummary(forceRefresh = false) {
    const box  = document.getElementById('ai-summary-body');
    const url  = `/restaurants/RESTAURANT_ID/summary${forceRefresh ? '?force=1' : ''}`;
    box.innerHTML = '<p class="ai-loading">⏳ Đang phân tích đánh giá...</p>';
    try {
        const res  = await fetch(url);
        const data = await res.json();
        if (data.error) {
            box.innerHTML = `<p class="ai-error">⚠️ ${data.error}</p>`;
            return;
        }
        const prosHTML = data.pros.map(p => `<li>✅ ${p}</li>`).join('');
        const consHTML = data.cons.length
            ? data.cons.map(c => `<li>⚠️ ${c}</li>`).join('')
            : '<li>Không có điểm chê nổi bật</li>';
        box.innerHTML = `
            <div class="ai-pros"><strong>Điểm khen</strong><ul>${prosHTML}</ul></div>
            <div class="ai-cons"><strong>Điểm chê</strong><ul>${consHTML}</ul></div>`;
    } catch {
        box.innerHTML = '<p class="ai-error">⚠️ Không thể tải tóm tắt lúc này.</p>';
    }
}
document.addEventListener('DOMContentLoaded', () => loadSummary());
document.getElementById('refresh-summary-btn')
    ?.addEventListener('click', () => loadSummary(true));
```

---

## 5. Giao diện khung tóm tắt (CSS)

```css
.ai-summary-box {
    background: linear-gradient(135deg, #fff9f9 0%, #fff4f4 100%);
    border: 1.5px solid #ffd5d5;
    border-left: 4px solid #FF6A6A;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
}
.ai-summary-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 800;
    color: #FF6A6A;
    margin-bottom: 1rem;
}
.ai-pros, .ai-cons { margin-bottom: .75rem; }
.ai-pros ul, .ai-cons ul { margin: .4rem 0 0 1rem; }
.ai-pros li, .ai-cons li { font-size: .88rem; margin-bottom: .3rem; }
.ai-loading, .ai-error { color: #999; font-size: .88rem; }
```

---

## 6. Cập nhật `.env.example`

```
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 7. Thư viện cần thêm vào `requirements.txt`

```
openai==1.40.0
```
