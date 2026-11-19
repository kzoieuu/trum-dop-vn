# Yêu cầu tính năng: AI Tóm tắt đánh giá quán ăn

**Dự án:** Trùm Đớp VN  
**Tính năng:** AI tóm tắt điểm khen và điểm chê của mỗi quán dựa trên đánh giá của khách hàng  
**Người dùng chính:** Khách hàng muốn chọn quán nhanh mà không cần đọc hết từng đánh giá  
**Phạm vi:** Nhóm 7 học sinh, hoàn thành trong 3 tuần  
**Công nghệ:** Python/Flask, SQLite, OpenAI API (ChatGPT), HTML/CSS/JS  

---

## 1. Bối cảnh

Trang chi tiết quán hiện có danh sách đánh giá dạng văn bản thô. Người dùng phải đọc nhiều nhận xét mới hiểu quán đó có gì tốt, gì chưa tốt. Tính năng này gọi OpenAI API để tự động tóm tắt toàn bộ đánh giá thành 2 mục ngắn gọn: **điểm khen** và **điểm chê**, giúp người dùng quyết định nhanh hơn.

---

## 2. Yêu cầu chức năng

### YC-01: Hiển thị khung tóm tắt AI trên trang chi tiết quán
- **Mô tả:** Trên trang `/restaurants/<id>`, phía trên danh sách đánh giá chi tiết, hiển thị một khung "🤖 Tóm tắt từ AI" gồm 2 phần: Điểm khen (✅) và Điểm chê (⚠️).
- **Tiêu chí chấp nhận (xong khi):**
  - Khung tóm tắt xuất hiện trên trang chi tiết của mọi quán có ít nhất 1 đánh giá.
  - Quán chưa có đánh giá nào thì hiện thông báo "Chưa có đủ đánh giá để tóm tắt."
  - Khung có thiết kế phù hợp màu `#FF6A6A` và font Nunito.

### YC-02: Gọi OpenAI API để tạo tóm tắt
- **Mô tả:** Hệ thống thu thập tất cả nội dung đánh giá của quán, gửi lên OpenAI API (model `gpt-4o-mini`), nhận về đoạn tóm tắt gồm điểm khen và điểm chê.
- **Tiêu chí chấp nhận (xong khi):**
  - Hệ thống gọi API thành công và nhận về kết quả dạng JSON gồm `pros` (danh sách điểm khen) và `cons` (danh sách điểm chê).
  - Mỗi mục khen/chê là 1 câu ngắn, tối đa 15 từ.
  - Nếu API lỗi hoặc timeout, hiển thị thông báo "Không thể tải tóm tắt lúc này, vui lòng thử lại sau."
  - Khóa API lưu trong `.env` với tên `OPENAI_API_KEY`, không xuất hiện trong code.

### YC-03: Lưu kết quả tóm tắt vào SQLite (cache)
- **Mô tả:** Sau khi nhận kết quả từ OpenAI, lưu vào bảng `ai_summaries` trong SQLite. Lần sau tải trang, dùng kết quả đã lưu thay vì gọi API lại — tiết kiệm chi phí.
- **Tiêu chí chấp nhận (xong khi):**
  - Bảng `ai_summaries` có các cột: `id`, `restaurant_id`, `pros`, `cons`, `review_count_at_summary`, `created_at`.
  - Lần đầu vào trang chi tiết: gọi API, lưu kết quả.
  - Lần sau vào cùng trang: đọc từ SQLite, không gọi API.
  - Khi quán có thêm đánh giá mới (số lượng thay đổi), tự động làm mới tóm tắt.

### YC-04: Nút "Làm mới tóm tắt"
- **Mô tả:** Người dùng có thể bấm nút để yêu cầu AI tóm tắt lại (khi có nhiều đánh giá mới).
- **Tiêu chí chấp nhận (xong khi):**
  - Có nút "🔄 Làm mới" nhỏ trong góc khung tóm tắt.
  - Bấm nút → gọi API lại → cập nhật kết quả trên trang và trong SQLite.
  - Trong lúc chờ AI phản hồi, hiển thị trạng thái loading (spinner hoặc chữ "Đang tóm tắt...").

### YC-05: Bảo vệ khóa API
- **Mô tả:** Khóa OpenAI API không được lộ ra ngoài dưới bất kỳ hình thức nào.
- **Tiêu chí chấp nhận (xong khi):**
  - `OPENAI_API_KEY` chỉ có trong file `.env` (không commit lên GitHub).
  - File `.env.example` có dòng `OPENAI_API_KEY=` (không có giá trị thật).
  - Toàn bộ logic gọi API nằm ở backend (Flask), không có khóa nào trong file JS phía client.

---

## 3. Yêu cầu phi chức năng

| Mục | Yêu cầu |
|---|---|
| Hiệu năng | Tóm tắt lần đầu tải xong trong vòng 10 giây |
| Chi phí | Dùng model `gpt-4o-mini` để tối thiểu chi phí API |
| Giao diện | Giữ nguyên font Nunito, màu `#FF6A6A`, không thêm thư viện CSS/JS mới |
| Bảo mật | Khóa API không được xuất hiện trong source code hoặc log |
| Tương thích | Chạy được trên Python 3.11+, Flask 3.0+ |

---

## 4. Ngoài phạm vi (không làm trong 3 tuần này)

- Phân tích cảm xúc theo từng khía cạnh (đồ ăn, phục vụ, giá cả riêng biệt)
- Tóm tắt đa ngôn ngữ
- Cho người dùng chọn độ dài tóm tắt
- Hiển thị tóm tắt trên trang danh sách quán
