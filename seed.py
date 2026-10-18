"""
Nạp dữ liệu mẫu từ wireframe vào SQLite.
Chạy: python seed.py
"""
from database import get_db, init_db

RESTAURANTS = [
    {
        'name': 'Phở Gia Truyền Phú Gia',
        'address': '146 Lý Chính Thắng, Phường 7, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3930 xxxx',
        'opening_hours': '06:00 – 11:00 | 17:00 – 22:00',
        'price_min': 45000,
        'price_max': 65000,
        'price_range': 'Bình dân',
        'food_type': 'Món nước',
        'description': 'Quán phở gia truyền với nước dùng đậm đà, thơm ngon theo công thức bí truyền nhiều đời.',
        'is_featured': 1,
        'rating': 4.8,
        'review_count': 120,
        'latitude': 10.7769,
        'longitude': 106.6951,
        'image_url': '',
    },
    {
        'name': 'Lẩu Nướng Phố – Chi nhánh Q.3',
        'address': '89 Võ Văn Tần, Phường 6, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3825 xxxx',
        'opening_hours': '10:00 – 22:00',
        'price_min': 150000,
        'price_max': 300000,
        'price_range': 'Tầm trung',
        'food_type': 'Lẩu & Nướng',
        'description': 'Chuyên lẩu nướng BBQ phong cách Hàn Quốc kết hợp Việt Nam, không gian rộng rãi, thoải mái.',
        'is_featured': 1,
        'rating': 4.5,
        'review_count': 87,
        'latitude': 10.7751,
        'longitude': 106.6923,
        'image_url': '',
    },
    {
        'name': 'Bánh mì & Cà phê Ông Vy',
        'address': '202 Nguyễn Thiện Thuật, Phường 3, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3526 xxxx',
        'opening_hours': '07:00 – 20:00',
        'price_min': 25000,
        'price_max': 55000,
        'price_range': 'Bình dân',
        'food_type': 'Ăn vặt',
        'description': 'Bánh mì thịt nướng giòn rụm, cà phê rang xay truyền thống, không gian cổ điển ấm cúng.',
        'is_featured': 0,
        'rating': 4.3,
        'review_count': 64,
        'latitude': 10.7738,
        'longitude': 106.6934,
        'image_url': '',
    },
    {
        'name': 'Hải Sản Đất Mũi',
        'address': '45 Đinh Tiên Hoàng, Phường Đa Kao, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3820 xxxx',
        'opening_hours': '10:30 – 22:30',
        'price_min': 200000,
        'price_max': 500000,
        'price_range': 'Tầm trung',
        'food_type': 'Hải sản',
        'description': 'Hải sản tươi sống nhập trực tiếp từ Cà Mau, chế biến theo nhiều kiểu: hấp, nướng, chiên giòn.',
        'is_featured': 1,
        'rating': 4.6,
        'review_count': 95,
        'latitude': 10.7878,
        'longitude': 106.7015,
        'image_url': '',
    },
    {
        'name': 'Lẩu Dê Lâm Ký',
        'address': '12 Trần Quý Khoách, Phường Tân Định, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3848 xxxx',
        'opening_hours': '11:00 – 23:00',
        'price_min': 120000,
        'price_max': 250000,
        'price_range': 'Tầm trung',
        'food_type': 'Lẩu & Nướng',
        'description': 'Chuyên lẩu dê với nước dùng nấu từ gừng và sả, thịt dê tươi mềm ngọt đặc trưng.',
        'is_featured': 0,
        'rating': 4.4,
        'review_count': 73,
        'latitude': 10.7892,
        'longitude': 106.6998,
        'image_url': '',
    },
    {
        'name': 'Hủ Tiếu Nam Vang Cô Giang',
        'address': '123 Cô Giang, Phường Cô Giang, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3836 xxxx',
        'opening_hours': '06:00 – 14:00',
        'price_min': 35000,
        'price_max': 55000,
        'price_range': 'Bình dân',
        'food_type': 'Món nước',
        'description': 'Hủ tiếu Nam Vang nước trong, ngọt tự nhiên với tôm thịt bằm và mực, ăn kèm giá sống.',
        'is_featured': 0,
        'rating': 4.7,
        'review_count': 108,
        'latitude': 10.7612,
        'longitude': 106.6889,
        'image_url': '',
    },
    {
        'name': 'Bún Bò Huế Chị Ba',
        'address': '67 Bà Huyện Thanh Quan, Phường 9, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3933 xxxx',
        'opening_hours': '06:30 – 13:00',
        'price_min': 40000,
        'price_max': 60000,
        'price_range': 'Bình dân',
        'food_type': 'Món nước',
        'description': 'Bún bò Huế cay nồng theo công thức gốc Huế, nước dùng đỏ thơm sả ớt, thịt bò mềm tan.',
        'is_featured': 0,
        'rating': 4.5,
        'review_count': 82,
        'latitude': 10.7744,
        'longitude': 106.6911,
        'image_url': '',
    },
    {
        'name': 'Cơm Tấm Sườn Bì Chả',
        'address': '234 Điện Biên Phủ, Phường 7, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3930 xxxx',
        'opening_hours': '07:00 – 21:00',
        'price_min': 45000,
        'price_max': 80000,
        'price_range': 'Bình dân',
        'food_type': 'Cơm',
        'description': 'Cơm tấm Sài Gòn chính hiệu: sườn nướng than thơm lừng, bì trộn dai giòn, chả hấp mịn màng.',
        'is_featured': 1,
        'rating': 4.6,
        'review_count': 91,
        'latitude': 10.7755,
        'longitude': 106.6945,
        'image_url': '',
    },
]

MENU_ITEMS = {
    'Phở Gia Truyền Phú Gia': [
        ('Phở tái', 45000),
        ('Phở Gia Truyền', 55000),
        ('Phở tái lăn', 50000),
        ('Phở bò viên', 45000),
        ('Phở gà', 50000),
        ('Phở nạm gân', 55000),
        ('Phở trộn', 40000),
        ('Quẩy nóng', 15000),
        ('Quẩy giòn', 15000),
        ('Nước ngọt', 15000),
        ('Trà đá', 5000),
    ],
    'Lẩu Nướng Phố – Chi nhánh Q.3': [
        ('Lẩu thái hải sản', 250000),
        ('Lẩu bò nhúng dấm', 220000),
        ('Lẩu nấm chay', 180000),
        ('Set thịt nướng BBQ', 199000),
        ('Tôm nướng muối ớt', 120000),
        ('Bạch tuộc nướng sa tế', 110000),
        ('Cơm chiên', 45000),
        ('Trà dâu', 35000),
    ],
    'Bánh mì & Cà phê Ông Vy': [
        ('Bánh mì thịt nướng', 30000),
        ('Bánh mì pate chả', 25000),
        ('Bánh mì trứng', 20000),
        ('Bánh mì đặc biệt', 35000),
        ('Cà phê đen', 20000),
        ('Cà phê sữa đá', 25000),
        ('Bạc xỉu', 25000),
        ('Sinh tố bơ', 35000),
    ],
}

REVIEWS = [
    {
        'restaurant_name': 'Phở Gia Truyền Phú Gia',
        'username': 'Minh Tuấn',
        'rating': 5,
        'content': 'Nước dùng ngon tuyệt, thịt mềm, quán sạch sẽ. Mình ăn ở đây từ nhỏ đến giờ vẫn không thay đổi.',
    },
    {
        'restaurant_name': 'Phở Gia Truyền Phú Gia',
        'username': 'Thu Hương',
        'rating': 5,
        'content': 'Phở bò ở đây số 1 Sài Gòn luôn! Buổi sáng hay đông khách lắm, nên đến sớm nhé.',
    },
    {
        'restaurant_name': 'Phở Gia Truyền Phú Gia',
        'username': 'Quốc Bảo',
        'rating': 4,
        'content': 'Ngon nhưng hơi đông, đôi khi phải chờ chỗ ngồi. Giá cả hợp lý so với chất lượng.',
    },
    {
        'restaurant_name': 'Lẩu Nướng Phố – Chi nhánh Q.3',
        'username': 'Lan Anh',
        'rating': 5,
        'content': 'Lẩu thái ở đây cực kỳ đậm đà, tôm cua tươi rói. Phù hợp đi nhóm đông bạn bè.',
    },
    {
        'restaurant_name': 'Hải Sản Đất Mũi',
        'username': 'Văn Khoa',
        'rating': 4,
        'content': 'Hải sản tươi, chế biến ngon. Giá hơi cao nhưng xứng đáng. Ghẹ hấp sả là món must-try!',
    },
]


def seed():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Xóa dữ liệu cũ để seed lại sạch
    cursor.execute('DELETE FROM menu_items')
    cursor.execute('DELETE FROM reviews')
    cursor.execute('DELETE FROM restaurants')

    # Nạp quán ăn
    restaurant_ids = {}
    for r in RESTAURANTS:
        cursor.execute('''
            INSERT INTO restaurants
            (name, address, district, phone, opening_hours,
             price_min, price_max, price_range, food_type, description,
             is_featured, rating, review_count, latitude, longitude, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            r['name'], r['address'], r['district'], r['phone'], r['opening_hours'],
            r['price_min'], r['price_max'], r['price_range'], r['food_type'], r['description'],
            r['is_featured'], r['rating'], r['review_count'],
            r['latitude'], r['longitude'], r['image_url'],
        ))
        restaurant_ids[r['name']] = cursor.lastrowid

    # Nạp menu
    for restaurant_name, items in MENU_ITEMS.items():
        rid = restaurant_ids.get(restaurant_name)
        if rid:
            for item_name, price in items:
                cursor.execute(
                    'INSERT INTO menu_items (restaurant_id, name, price) VALUES (?, ?, ?)',
                    (rid, item_name, price)
                )

    # Nạp đánh giá mẫu
    for rv in REVIEWS:
        rid = restaurant_ids.get(rv['restaurant_name'])
        if rid:
            cursor.execute(
                'INSERT INTO reviews (restaurant_id, username, rating, content) VALUES (?, ?, ?, ?)',
                (rid, rv['username'], rv['rating'], rv['content'])
            )

    conn.commit()
    conn.close()
    print(f'Đã nạp {len(RESTAURANTS)} quán ăn, menu và đánh giá mẫu.')


if __name__ == '__main__':
    seed()
