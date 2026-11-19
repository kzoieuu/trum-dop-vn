# Danh sách việc cần làm: AI Tóm tắt đánh giá quán ăn

**Dự án:** Trùm Đớp VN  
**Tổng thời gian:** 3 tuần (mỗi buổi ~2–3 giờ)  
**Nhóm:** 7 thành viên  

> Mỗi task đủ nhỏ để làm xong trong 1 buổi.  
> Ghi tên người phụ trách vào cột "Phụ trách" trước khi bắt đầu.

---

## TUẦN 1 — Chuẩn bị và Backend

### Task 01 — Lấy khóa OpenAI API
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Đăng ký tài khoản OpenAI, lấy API key, thêm vào file `.env` với tên `OPENAI_API_KEY`. Cập nhật `.env.example` thêm dòng `OPENAI_API_KEY=`.
- **Xong khi:** Chạy đoạn test Python gọi được API và nhận về phản hồi, không lộ key trong code.
- **Lưu ý:** Vào https://platform.openai.com → API keys → Create new key.

### Task 02 — Tạo bảng `ai_summaries` trong database
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Thêm câu lệnh `CREATE TABLE IF NOT EXISTS ai_summaries` vào `database.py` theo đúng schema trong `design.md`.
- **Xong khi:** Chạy `python database.py` không báo lỗi; mở file `.db` kiểm tra thấy bảng `ai_summaries` với đủ các cột.

### Task 03 — Viết file `ai_summary.py` (hàm gọi API)
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Tạo file `ai_summary.py`, viết hàm `get_or_create_summary()` theo thiết kế trong `design.md`. Hàm đọc cache từ SQLite trước, chỉ gọi API khi cần.
- **Xong khi:** Gọi hàm với dữ liệu thử nghiệm, nhận về dict `{"pros": [...], "cons": [...]}` đúng format.

### Task 04 — Thêm route `/restaurants/<id>/summary` vào `app.py`
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Thêm 2 route mới vào `app.py`: `GET /restaurants/<id>/summary` (trả JSON) và `POST /restaurants/<id>/summary/refresh` (xóa cache, tạo mới). Import `ai_summary.py` trong route.
- **Xong khi:** Dùng trình duyệt hoặc curl truy cập `/restaurants/1/summary`, nhận về JSON hợp lệ gồm `pros` và `cons`.

### Task 05 — Xử lý lỗi API (timeout, hết quota, key sai)
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Bọc toàn bộ lệnh gọi OpenAI trong `try/except`, trả về `{"error": "..."}` khi lỗi. Thêm timeout 15 giây cho request.
- **Xong khi:** Thử truyền key sai → route trả về JSON lỗi thay vì crash server.

---

## TUẦN 2 — Frontend và Giao diện

### Task 06 — Thêm khung tóm tắt AI vào `restaurant_detail.html`
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Thêm div `ai-summary-box` vào đúng vị trí trong template (phía trên danh sách đánh giá). Thêm nút "🔄 Làm mới" trong header khung.
- **Xong khi:** Vào trang chi tiết bất kỳ quán, thấy khung tóm tắt xuất hiện đúng vị trí (dù chưa có dữ liệu).

### Task 07 — Viết CSS cho khung tóm tắt
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Thêm CSS cho `.ai-summary-box`, `.ai-summary-header`, `.ai-pros`, `.ai-cons`, `.ai-loading`, `.ai-error` vào `style.css` theo thiết kế trong `design.md`. Giữ đúng màu `#FF6A6A` và font Nunito.
- **Xong khi:** Khung trông đẹp, nhất quán với giao diện web hiện tại, hiển thị tốt trên cả máy tính và điện thoại.

### Task 08 — Viết JS gọi API và hiển thị kết quả
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Thêm hàm `loadSummary()` trong block `extra_js` của `restaurant_detail.html`. Hàm dùng `fetch()` gọi route `/summary`, phân tích JSON và render HTML điểm khen/chê vào khung.
- **Xong khi:** Vào trang chi tiết quán → khung tự động tải, hiển thị điểm khen và điểm chê đúng định dạng.

### Task 09 — Hiển thị trạng thái loading và lỗi
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Trong khi chờ API phản hồi hiện "⏳ Đang phân tích đánh giá...". Nếu lỗi hiện "⚠️ Không thể tải tóm tắt lúc này, vui lòng thử lại sau." Nếu quán chưa có đánh giá hiện "Chưa có đủ đánh giá để tóm tắt."
- **Xong khi:** Thử 3 trường hợp: quán có đánh giá, quán không có đánh giá, cắt mạng → đều hiển thị đúng thông báo tương ứng.

### Task 10 — Nút "🔄 Làm mới tóm tắt"
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Gán sự kiện click cho nút "🔄 Làm mới": gọi lại `loadSummary(true)` với tham số `force=1`, route xóa cache và gọi API mới.
- **Xong khi:** Bấm "Làm mới" → khung hiện loading → sau vài giây cập nhật tóm tắt mới.

---

## TUẦN 3 — Kiểm thử và Hoàn thiện

### Task 11 — Kiểm thử tích hợp toàn luồng
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Chạy thử toàn bộ luồng: vào trang chi tiết lần 1 (gọi API), vào lần 2 (đọc cache), thêm đánh giá mới (tóm tắt tự làm mới), bấm nút làm mới thủ công.
- **Xong khi:** Cả 4 trường hợp hoạt động đúng, không có lỗi nào xuất hiện trong console.

### Task 12 — Kiểm tra bảo mật khóa API
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Kiểm tra `OPENAI_API_KEY` không xuất hiện trong: source code HTML (F12 → View Source), file JS, response JSON từ server, git log.
- **Xong khi:** Không tìm thấy key ở bất kỳ đâu ngoài file `.env` trên máy local.

### Task 13 — Kiểm thử trên điện thoại và nhiều trình duyệt
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Mở web trên Chrome, Edge và điện thoại (dùng link Render). Kiểm tra khung tóm tắt hiển thị đúng, không bị vỡ layout.
- **Xong khi:** Giao diện đẹp và chức năng hoạt động đúng trên cả 3 môi trường.

### Task 14 — Push code lên GitHub và deploy Render
- **Phụ trách:** _(điền tên)_
- **Mô tả:** Commit toàn bộ thay đổi, push lên GitHub. Thêm `OPENAI_API_KEY` vào Environment Variables trên Render (không commit key). Chờ Render deploy lại và kiểm tra web chạy đúng.
- **Xong khi:** Web tại `https://trum-dop-vn.onrender.com` hiển thị tóm tắt AI hoạt động đúng.

---

## Tổng quan phân công (mỗi bạn ít nhất 2 task)

| Thành viên | Task phụ trách |
|---|---|
| Thành viên 1 | Task 01, Task 06 |
| Thành viên 2 | Task 02, Task 07 |
| Thành viên 3 | Task 03, Task 08 |
| Thành viên 4 | Task 04, Task 09 |
| Thành viên 5 | Task 05, Task 10 |
| Thành viên 6 | Task 11, Task 12 |
| Thành viên 7 | Task 13, Task 14 |

> Điền tên thật của từng bạn vào bảng trên trước khi bắt đầu tuần 1.
