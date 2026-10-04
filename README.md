# 🦉 ForFriend — Nền Tảng Tìm Bạn Học Nhóm Sinh Viên

> **Đồ án môn học**: Course Project TIN314  
> **Phong cách**: Retro Game Pixel Art (Dark Theme Neon)  
> **Tech Stack**: 100% Pure Python (FastAPI + Reflex + SQLite Async)  
> **Repository GitHub**: [https://github.com/TIN314-Nhom10/forfriend](https://github.com/TIN314-Nhom10/forfriend)

---

## 1. Tổng Quan Dự Án (Project Overview)

**ForFriend** là nền tảng kết nối học tập dành cho sinh viên, hỗ trợ:
- **Offline (Quest Board)**: Đăng tin tìm bạn học theo trường, môn học, khu vực với thuật toán matching tương đồng thông minh.
- **Online (Adventure Zones)**: Phòng học ảo với tính năng xin vào (knock-to-enter) và video call tích hợp **LiveKit WebRTC**.
- **Chat & Friends**: Quán trọ bạn bè, nhắn tin 1-1 real-time và hệ thống đánh giá uy tín sau buổi học.
- **AI Verification**: Tích hợp Google Gemini AI OCR kiểm tra thẻ sinh viên tự động.

---

## 2. Triển Khai Cloud Miễn Phí 24/7 (Deploy to Render.com)

Dự án đã tích hợp sẵn **`Dockerfile`**, **`Caddyfile`** và **`render.yaml`** để triển khai trọn gói cả Backend + Frontend + Database chỉ trong 1 Web Service duy nhất (hoàn toàn miễn phí trên Render):

### Các bước triển khai:
1. Đăng ký/Đăng nhập tại [Render.com](https://render.com) bằng tài khoản **GitHub**.
2. Tại trang Dashboard, chọn **New +** ➔ **Blueprint** (hoặc **Web Service**).
3. Chọn Repository: `TIN314-Nhom10/forfriend`.
4. Render sẽ tự động nhận diện file **`render.yaml`** và cấu hình môi trường.
5. Nhấn **Apply** (hoặc **Deploy**). Render sẽ tự động build image và khởi động server.
6. Sau khi hoàn tất (khoảng 3–5 phút), Render sẽ cấp đường dẫn Live Demo công khai:
   - **Web App**: `https://<ten-app>.onrender.com/`
   - **Swagger API Docs**: `https://<ten-app>.onrender.com/docs`

---

## 3. Khởi Chạy Nhanh Trên Máy Tính (Local Run)

### Cách 1: Khởi chạy 1-Click (Khuyên dùng khi chấm bài)

- **Trên Windows**: Nhấp đúp chuột vào file:
  ```cmd
  .\run_dev.bat
  ```
- **Trên Linux / macOS**:
  ```bash
  chmod +x run_dev.sh && ./run_dev.sh
  ```

Địa chỉ truy cập:
- **Frontend Web**: `http://localhost:3000` (hoặc truy cập qua mạng LAN: `http://<LAN_IP>:3000`)
- **Backend API & Swagger Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

---

### Cách 2: Khởi chạy thủ công từng dịch vụ

```bash
# 1. Tạo & kích hoạt virtual environment
python -m venv .venv
# Windows: .\.venv\Scripts\activate | Linux/macOS: source .venv/bin/activate

# 2. Cài đặt thư viện
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 3. Khởi tạo database và nạp dữ liệu mẫu
cd backend && python -m app.init_db && cd ..

# 4. Chạy Backend (Terminal 1)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Chạy Frontend (Terminal 2)
cd frontend && reflex run
```

---

## 4. Tài Khoản Demo Sẵn Có (Test Accounts)

Hệ thống đã nạp sẵn các tài khoản sinh viên mẫu:

| Email | Mật khẩu | Trường | Chuyên ngành / Lĩnh vực |
|:---|:---|:---|:---|
| `nguyenvana@ftu.edu.vn` | `Password123!` | ĐH Ngoại Thương Hà Nội | CNTT & Toán (Level 3) |
| `tranthib@neu.edu.vn` | `Password123!` | ĐH Kinh tế Quốc dân | Kinh tế & Ngoại ngữ (Level 2) |
| `liam@forfriend.local` | `Password123!` | Gaming headphones | Computer Science (Level 5) |
| `chloe@forfriend.local` | `Password123!` | Reading | Mathematics (Level 4) |

> *Gợi ý: Tại màn hình Đăng nhập, có thể bấm nút **"Demo Login (FTU Student)"** để đăng nhập ngay mà không cần gõ mật khẩu.*

---

## 5. Tài Liệu Thiết Kế Kỹ Thuật

Tài liệu kiến trúc chi tiết, sơ đồ cơ sở dữ liệu và đặc tả API được lưu trữ trong thư mục [`docs/`](./docs/):
- [`00-overview.md`](./docs/00-overview.md): Tổng quan kiến trúc & Tech stack
- [`01-architecture.md`](./docs/01-architecture.md): Sơ đồ luồng dữ liệu & sequence diagrams
- [`02-database-schema.md`](./docs/02-database-schema.md): Thiết kế 10 bảng SQLite
- [`03-api-design.md`](./docs/03-api-design.md): Đặc tả API REST & WebSockets
