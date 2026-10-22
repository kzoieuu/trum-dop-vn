"""
Nạp dữ liệu mẫu vào SQLite.
Chạy: python seed.py
"""
from database import get_db, init_db

RESTAURANTS = [
    # ── Quận 1 ──────────────────────────────────────────
    {
        'name': 'Phở Lệ',
        'address': '413 Nguyễn Trãi, Phường Nguyễn Cư Trinh, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3836 3585',
        'opening_hours': '06:00 – 22:00',
        'price_min': 55000, 'price_max': 80000,
        'price_range': 'Bình dân', 'food_type': 'Món nước',
        'description': 'Phở bò nổi tiếng Sài Gòn, nước dùng trong vắt ngọt tự nhiên, thịt bò tươi mềm.',
        'is_featured': 1, 'rating': 4.7, 'review_count': 215,
        'latitude': 10.7631, 'longitude': 106.6855, 'image_url': '',
    },
    {
        'name': 'Hải Sản Đất Mũi',
        'address': '45 Đinh Tiên Hoàng, Phường Đa Kao, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3820 xxxx',
        'opening_hours': '10:30 – 22:30',
        'price_min': 200000, 'price_max': 500000,
        'price_range': 'Tầm trung', 'food_type': 'Hải sản',
        'description': 'Hải sản tươi sống nhập trực tiếp từ Cà Mau, chế biến theo nhiều kiểu: hấp, nướng, chiên giòn.',
        'is_featured': 1, 'rating': 4.6, 'review_count': 95,
        'latitude': 10.7878, 'longitude': 106.7015, 'image_url': '',
    },
    {
        'name': 'Hủ Tiếu Nam Vang Cô Giang',
        'address': '123 Cô Giang, Phường Cô Giang, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3836 xxxx',
        'opening_hours': '06:00 – 14:00',
        'price_min': 35000, 'price_max': 55000,
        'price_range': 'Bình dân', 'food_type': 'Món nước',
        'description': 'Hủ tiếu Nam Vang nước trong, ngọt tự nhiên với tôm thịt bằm và mực, ăn kèm giá sống.',
        'is_featured': 0, 'rating': 4.7, 'review_count': 108,
        'latitude': 10.7612, 'longitude': 106.6889, 'image_url': '',
    },
    {
        'name': 'Lẩu Dê Lâm Ký',
        'address': '12 Trần Quý Khoách, Phường Tân Định, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3848 xxxx',
        'opening_hours': '11:00 – 23:00',
        'price_min': 120000, 'price_max': 250000,
        'price_range': 'Tầm trung', 'food_type': 'Lẩu & Nướng',
        'description': 'Chuyên lẩu dê với nước dùng nấu từ gừng và sả, thịt dê tươi mềm ngọt đặc trưng.',
        'is_featured': 0, 'rating': 4.4, 'review_count': 73,
        'latitude': 10.7892, 'longitude': 106.6998, 'image_url': '',
    },
    {
        'name': 'Kem Bách Đằng',
        'address': '26-28 Lê Lợi, Phường Bến Nghé, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3829 2942',
        'opening_hours': '07:00 – 22:00',
        'price_min': 25000, 'price_max': 65000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Kem cây, kem tươi và chè thập cẩm nổi tiếng Sài Gòn từ thập niên 60. Không gian cổ điển mát mẻ.',
        'is_featured': 1, 'rating': 4.5, 'review_count': 188,
        'latitude': 10.7726, 'longitude': 106.7034, 'image_url': '',
    },
    {
        'name': 'Chè Hiển Khánh',
        'address': '187 Cống Quỳnh, Phường Nguyễn Cư Trinh, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3833 xxxx',
        'opening_hours': '08:00 – 23:00',
        'price_min': 20000, 'price_max': 45000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Chè thập cẩm, chè đậu xanh, chè khúc bạch và các loại chè truyền thống Nam Bộ.',
        'is_featured': 0, 'rating': 4.3, 'review_count': 92,
        'latitude': 10.7658, 'longitude': 106.6901, 'image_url': '',
    },
    {
        'name': 'Bánh Mì Huỳnh Hoa',
        'address': '26 Lê Thị Riêng, Phường Bến Thành, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3925 xxxx',
        'opening_hours': '14:00 – 23:00',
        'price_min': 40000, 'price_max': 60000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Bánh mì thịt nguội nổi tiếng nhất Sài Gòn, nhân đầy ắp, vỏ giòn rụm, thường xuyên có hàng dài chờ.',
        'is_featured': 1, 'rating': 4.8, 'review_count': 342,
        'latitude': 10.7716, 'longitude': 106.6963, 'image_url': '',
    },
    {
        'name': 'Cơm Tấm Thuận Kiều',
        'address': '180 Nguyễn Công Trứ, Phường Nguyễn Thái Bình, Quận 1',
        'district': 'Quận 1',
        'phone': '028 3914 xxxx',
        'opening_hours': '06:00 – 22:00',
        'price_min': 45000, 'price_max': 85000,
        'price_range': 'Bình dân', 'food_type': 'Cơm',
        'description': 'Cơm tấm sườn bì chả Sài Gòn truyền thống, sườn nướng than thơm lừng, nước mắm pha chuẩn vị.',
        'is_featured': 0, 'rating': 4.4, 'review_count': 67,
        'latitude': 10.7689, 'longitude': 106.6977, 'image_url': '',
    },

    # ── Quận 3 ──────────────────────────────────────────
    {
        'name': 'Phở Gia Truyền Phú Gia',
        'address': '146 Lý Chính Thắng, Phường 7, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3930 xxxx',
        'opening_hours': '06:00 – 11:00 | 17:00 – 22:00',
        'price_min': 45000, 'price_max': 65000,
        'price_range': 'Bình dân', 'food_type': 'Món nước',
        'description': 'Quán phở gia truyền với nước dùng đậm đà, thơm ngon theo công thức bí truyền nhiều đời.',
        'is_featured': 1, 'rating': 4.8, 'review_count': 120,
        'latitude': 10.7769, 'longitude': 106.6951, 'image_url': '',
    },
    {
        'name': 'Lẩu Nướng Phố – Chi nhánh Q.3',
        'address': '89 Võ Văn Tần, Phường 6, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3825 xxxx',
        'opening_hours': '10:00 – 22:00',
        'price_min': 150000, 'price_max': 300000,
        'price_range': 'Tầm trung', 'food_type': 'Lẩu & Nướng',
        'description': 'Chuyên lẩu nướng BBQ phong cách Hàn Quốc kết hợp Việt Nam, không gian rộng rãi.',
        'is_featured': 1, 'rating': 4.5, 'review_count': 87,
        'latitude': 10.7751, 'longitude': 106.6923, 'image_url': '',
    },
    {
        'name': 'Bánh mì & Cà phê Ông Vy',
        'address': '202 Nguyễn Thiện Thuật, Phường 3, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3526 xxxx',
        'opening_hours': '07:00 – 20:00',
        'price_min': 25000, 'price_max': 55000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Bánh mì thịt nướng giòn rụm, cà phê rang xay truyền thống, không gian cổ điển ấm cúng.',
        'is_featured': 0, 'rating': 4.3, 'review_count': 64,
        'latitude': 10.7738, 'longitude': 106.6934, 'image_url': '',
    },
    {
        'name': 'Bún Bò Huế Chị Ba',
        'address': '67 Bà Huyện Thanh Quan, Phường 9, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3933 xxxx',
        'opening_hours': '06:30 – 13:00',
        'price_min': 40000, 'price_max': 60000,
        'price_range': 'Bình dân', 'food_type': 'Món nước',
        'description': 'Bún bò Huế cay nồng theo công thức gốc Huế, nước dùng đỏ thơm sả ớt.',
        'is_featured': 0, 'rating': 4.5, 'review_count': 82,
        'latitude': 10.7744, 'longitude': 106.6911, 'image_url': '',
    },
    {
        'name': 'Cơm Tấm Sườn Bì Chả',
        'address': '234 Điện Biên Phủ, Phường 7, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3930 xxxx',
        'opening_hours': '07:00 – 21:00',
        'price_min': 45000, 'price_max': 80000,
        'price_range': 'Bình dân', 'food_type': 'Cơm',
        'description': 'Cơm tấm Sài Gòn chính hiệu: sườn nướng than thơm lừng, bì trộn dai giòn.',
        'is_featured': 1, 'rating': 4.6, 'review_count': 91,
        'latitude': 10.7755, 'longitude': 106.6945, 'image_url': '',
    },
    {
        'name': 'Trà Sữa Gong Cha Quận 3',
        'address': '150 Nam Kỳ Khởi Nghĩa, Phường 4, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3822 xxxx',
        'opening_hours': '08:00 – 22:30',
        'price_min': 45000, 'price_max': 85000,
        'price_range': 'Tầm trung', 'food_type': 'Ăn vặt',
        'description': 'Trà sữa Đài Loan chính hiệu, trân châu dai mềm, topping đa dạng, không gian trẻ trung.',
        'is_featured': 0, 'rating': 4.4, 'review_count': 156,
        'latitude': 10.7762, 'longitude': 106.6918, 'image_url': '',
    },
    {
        'name': 'Nhà Hàng Chay Loving Hut',
        'address': '37D Nguyễn Thị Minh Khai, Phường 6, Quận 3',
        'district': 'Quận 3',
        'phone': '028 3822 5085',
        'opening_hours': '07:00 – 21:00',
        'price_min': 35000, 'price_max': 90000,
        'price_range': 'Bình dân', 'food_type': 'Món chay',
        'description': 'Buffet và món chay đa dạng, thực phẩm tươi sạch, không gian yên tĩnh phù hợp ăn chay hàng ngày.',
        'is_featured': 0, 'rating': 4.3, 'review_count': 74,
        'latitude': 10.7781, 'longitude': 106.6902, 'image_url': '',
    },

    # ── Quận 10 ──────────────────────────────────────────
    {
        'name': 'Bánh Cuốn Tây Hồ',
        'address': '34 Đinh Tiên Hoàng, Phường 1, Quận 10',
        'district': 'Quận 10',
        'phone': '028 3832 xxxx',
        'opening_hours': '06:00 – 14:00',
        'price_min': 30000, 'price_max': 55000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Bánh cuốn Hà Nội chính gốc, vỏ bánh mỏng mịn, nhân thịt mộc nhĩ thơm ngon, chả lụa giòn.',
        'is_featured': 0, 'rating': 4.5, 'review_count': 103,
        'latitude': 10.7712, 'longitude': 106.6678, 'image_url': '',
    },
    {
        'name': 'Bún Riêu Cua Bà Bảy',
        'address': '210 Lý Thường Kiệt, Phường 14, Quận 10',
        'district': 'Quận 10',
        'phone': '028 3865 xxxx',
        'opening_hours': '06:00 – 13:00',
        'price_min': 40000, 'price_max': 60000,
        'price_range': 'Bình dân', 'food_type': 'Món nước',
        'description': 'Bún riêu cua đồng nguyên chất, nước dùng đỏ cà chua thơm chua ngọt tự nhiên.',
        'is_featured': 0, 'rating': 4.6, 'review_count': 88,
        'latitude': 10.7701, 'longitude': 106.6689, 'image_url': '',
    },
    {
        'name': 'Lẩu Cá Kèo Vân Long',
        'address': '98 Ngô Gia Tự, Phường 2, Quận 10',
        'district': 'Quận 10',
        'phone': '028 3868 xxxx',
        'opening_hours': '10:00 – 22:00',
        'price_min': 180000, 'price_max': 350000,
        'price_range': 'Tầm trung', 'food_type': 'Lẩu & Nướng',
        'description': 'Lẩu cá kèo lá giang đặc sản miền Tây, cá tươi sống, nước lẩu chua thanh đậm vị.',
        'is_featured': 1, 'rating': 4.7, 'review_count': 134,
        'latitude': 10.7723, 'longitude': 106.6701, 'image_url': '',
    },
    {
        'name': 'Xôi Gà Bà Ký',
        'address': '55 Tô Hiến Thành, Phường 15, Quận 10',
        'district': 'Quận 10',
        'phone': '028 3862 xxxx',
        'opening_hours': '05:30 – 11:00',
        'price_min': 25000, 'price_max': 50000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Xôi gà xé, xôi lạp xưởng, xôi mặn truyền thống Sài Gòn, ăn sáng no bụng giá bình dân.',
        'is_featured': 0, 'rating': 4.4, 'review_count': 77,
        'latitude': 10.7734, 'longitude': 106.6712, 'image_url': '',
    },
    {
        'name': 'Kem Tươi Cây Dừa',
        'address': '125 Nguyễn Chí Thanh, Phường 9, Quận 10',
        'district': 'Quận 10',
        'phone': '028 3855 xxxx',
        'opening_hours': '09:00 – 22:00',
        'price_min': 20000, 'price_max': 55000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Kem tươi, kem cuộn, kem chiên và các loại kem đặc biệt, không gian mát mẻ dễ chịu.',
        'is_featured': 0, 'rating': 4.3, 'review_count': 61,
        'latitude': 10.7698, 'longitude': 106.6668, 'image_url': '',
    },

    # ── Quận Bình Thạnh ──────────────────────────────────
    {
        'name': 'Lẩu Bò Tự Do',
        'address': '246 Đinh Bộ Lĩnh, Phường 26, Quận Bình Thạnh',
        'district': 'Quận Bình Thạnh',
        'phone': '028 3899 xxxx',
        'opening_hours': '10:00 – 22:30',
        'price_min': 160000, 'price_max': 320000,
        'price_range': 'Tầm trung', 'food_type': 'Lẩu & Nướng',
        'description': 'Lẩu bò nhúng dấm và nướng vỉ than hoa, thịt bò Úc tươi mềm, nước dùng đậm đà.',
        'is_featured': 1, 'rating': 4.6, 'review_count': 112,
        'latitude': 10.8156, 'longitude': 106.7089, 'image_url': '',
    },
    {
        'name': 'Hủ Tiếu Nam Vang Bình Thạnh',
        'address': '320 Bạch Đằng, Phường 14, Quận Bình Thạnh',
        'district': 'Quận Bình Thạnh',
        'phone': '028 3840 xxxx',
        'opening_hours': '06:00 – 14:00',
        'price_min': 35000, 'price_max': 60000,
        'price_range': 'Bình dân', 'food_type': 'Món nước',
        'description': 'Hủ tiếu Nam Vang đặc trưng với gan heo, tôm, mực và thịt bằm, nước dùng ngọt thanh.',
        'is_featured': 0, 'rating': 4.5, 'review_count': 98,
        'latitude': 10.8112, 'longitude': 106.7067, 'image_url': '',
    },
    {
        'name': 'Cơm Gà Xối Mỡ Đông Nguyên',
        'address': '102 Nơ Trang Long, Phường 12, Quận Bình Thạnh',
        'district': 'Quận Bình Thạnh',
        'phone': '028 3841 xxxx',
        'opening_hours': '09:00 – 21:00',
        'price_min': 50000, 'price_max': 90000,
        'price_range': 'Bình dân', 'food_type': 'Cơm',
        'description': 'Cơm gà xối mỡ giòn rụm, thịt gà mềm ngọt, cơm trắng dẻo, nước mắm gừng đặc trưng.',
        'is_featured': 0, 'rating': 4.4, 'review_count': 85,
        'latitude': 10.8089, 'longitude': 106.7045, 'image_url': '',
    },
    {
        'name': 'Trà Sữa The Alley Bình Thạnh',
        'address': '51 Phan Đình Phùng, Phường 2, Quận Bình Thạnh',
        'district': 'Quận Bình Thạnh',
        'phone': '028 3803 xxxx',
        'opening_hours': '09:00 – 22:00',
        'price_min': 55000, 'price_max': 95000,
        'price_range': 'Tầm trung', 'food_type': 'Ăn vặt',
        'description': 'Thương hiệu trà sữa Đài Loan cao cấp, trân châu đường đen thủ công, không gian hiện đại.',
        'is_featured': 0, 'rating': 4.5, 'review_count': 143,
        'latitude': 10.8023, 'longitude': 106.7012, 'image_url': '',
    },
    {
        'name': 'Bánh Tráng Trộn Bình Thạnh',
        'address': '78 Hoàng Hoa Thám, Phường 12, Quận Bình Thạnh',
        'district': 'Quận Bình Thạnh',
        'phone': '',
        'opening_hours': '14:00 – 22:00',
        'price_min': 15000, 'price_max': 35000,
        'price_range': 'Bình dân', 'food_type': 'Ăn vặt',
        'description': 'Bánh tráng trộn chua cay mặn ngọt đặc trưng, khô bò dai thơm, tàu hũ ky giòn, trứng cút.',
        'is_featured': 0, 'rating': 4.3, 'review_count': 55,
        'latitude': 10.8067, 'longitude': 106.7034, 'image_url': '',
    },
    {
        'name': 'Nhà Hàng Hải Sản Biển Đông',
        'address': '168 Nguyễn Xí, Phường 26, Quận Bình Thạnh',
        'district': 'Quận Bình Thạnh',
        'phone': '028 3895 xxxx',
        'opening_hours': '10:00 – 22:00',
        'price_min': 250000, 'price_max': 600000,
        'price_range': 'Cao cấp', 'food_type': 'Hải sản',
        'description': 'Nhà hàng hải sản cao cấp, bể cá sống ngay tại bàn, chế biến theo yêu cầu của khách.',
        'is_featured': 1, 'rating': 4.7, 'review_count': 167,
        'latitude': 10.8134, 'longitude': 106.7078, 'image_url': '',
    },
]

MENU_ITEMS = {
    'Phở Gia Truyền Phú Gia': [
        ('Phở tái', 45000), ('Phở Gia Truyền', 55000), ('Phở tái lăn', 50000),
        ('Phở bò viên', 45000), ('Phở gà', 50000), ('Phở nạm gân', 55000),
        ('Phở trộn', 40000), ('Quẩy nóng', 15000), ('Trà đá', 5000),
    ],
    'Phở Lệ': [
        ('Phở tái', 55000), ('Phở chín', 55000), ('Phở tái nạm', 65000),
        ('Phở bò viên', 60000), ('Phở gà', 60000), ('Quẩy', 15000), ('Trà đá', 5000),
    ],
    'Lẩu Nướng Phố – Chi nhánh Q.3': [
        ('Lẩu thái hải sản', 250000), ('Lẩu bò nhúng dấm', 220000),
        ('Set thịt nướng BBQ', 199000), ('Tôm nướng muối ớt', 120000),
        ('Cơm chiên', 45000), ('Trà dâu', 35000),
    ],
    'Bánh mì & Cà phê Ông Vy': [
        ('Bánh mì thịt nướng', 30000), ('Bánh mì pate chả', 25000),
        ('Bánh mì đặc biệt', 35000), ('Cà phê đen', 20000),
        ('Cà phê sữa đá', 25000), ('Bạc xỉu', 25000),
    ],
    'Kem Bách Đằng': [
        ('Kem cây các loại', 25000), ('Kem tươi', 35000), ('Chè thập cẩm', 45000),
        ('Chè đậu xanh', 30000), ('Sinh tố bơ', 50000), ('Nước mía', 20000),
    ],
    'Bánh Mì Huỳnh Hoa': [
        ('Bánh mì đặc biệt', 55000), ('Bánh mì thịt', 45000),
        ('Bánh mì chả', 40000), ('Bánh mì trứng', 35000),
    ],
    'Xôi Gà Bà Ký': [
        ('Xôi gà xé', 35000), ('Xôi lạp xưởng', 30000),
        ('Xôi mặn', 25000), ('Xôi đậu phộng', 20000),
    ],
    'Kem Tươi Cây Dừa': [
        ('Kem cuộn', 45000), ('Kem chiên', 40000), ('Kem tươi que', 25000),
        ('Kem ly', 35000), ('Sinh tố kem', 55000),
    ],
    'Bánh Cuốn Tây Hồ': [
        ('Bánh cuốn nhân thịt', 40000), ('Bánh cuốn trứng', 45000),
        ('Bánh cuốn không nhân', 35000), ('Chả lụa', 20000), ('Trà đá', 5000),
    ],
    'Bún Riêu Cua Bà Bảy': [
        ('Bún riêu cua', 45000), ('Bún riêu tôm', 50000),
        ('Bún riêu đặc biệt', 60000), ('Trà đá', 5000),
    ],
}

REVIEWS = [
    {'restaurant_name': 'Phở Gia Truyền Phú Gia', 'username': 'Minh Tuấn',
     'rating': 5, 'content': 'Nước dùng ngon tuyệt, thịt mềm, quán sạch sẽ!'},
    {'restaurant_name': 'Phở Gia Truyền Phú Gia', 'username': 'Thu Hương',
     'rating': 5, 'content': 'Phở bò ở đây số 1 Sài Gòn luôn!'},
    {'restaurant_name': 'Phở Lệ', 'username': 'Khánh Linh',
     'rating': 5, 'content': 'Phở Lệ nổi tiếng có lý do, nước dùng trong và ngọt tự nhiên.'},
    {'restaurant_name': 'Kem Bách Đằng', 'username': 'Bảo Châu',
     'rating': 5, 'content': 'Kem Bách Đằng tuổi thơ! Không gian cổ điển, kem ngon vẫn như xưa.'},
    {'restaurant_name': 'Bánh Mì Huỳnh Hoa', 'username': 'Hoàng Nam',
     'rating': 5, 'content': 'Xếp hàng 20 phút nhưng xứng đáng! Nhân bánh đầy ắp, giòn rụm.'},
    {'restaurant_name': 'Lẩu Cá Kèo Vân Long', 'username': 'Thanh Mai',
     'rating': 5, 'content': 'Lẩu cá kèo lá giang ngon xuất sắc, đặc sản miền Tây hiếm thấy ở Sài Gòn.'},
    {'restaurant_name': 'Nhà Hàng Hải Sản Biển Đông', 'username': 'Văn Khoa',
     'rating': 4, 'content': 'Hải sản tươi sống, chế biến đúng chuẩn, giá cao nhưng xứng đáng.'},
]


def seed():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM menu_items')
    cursor.execute('DELETE FROM reviews')
    cursor.execute('DELETE FROM restaurants')

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

    for restaurant_name, items in MENU_ITEMS.items():
        rid = restaurant_ids.get(restaurant_name)
        if rid:
            for item_name, price in items:
                cursor.execute(
                    'INSERT INTO menu_items (restaurant_id, name, price) VALUES (?, ?, ?)',
                    (rid, item_name, price)
                )

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
