# 🦉 ForFriend — Nền Tảng Tìm Bạn Học Nhóm Sinh Viên

> **100% Pure Python Stack: FastAPI + Reflex + SQLite (Zero Docker, Zero Redis)**

---

## 1. Overview (Tổng Quan)

**ForFriend** là nền tảng kết nối học tập dành cho sinh viên:
- **Offline (Quest Board)**: Đăng tin và tìm kiếm bạn học theo trường, môn học, địa điểm với thuật toán gợi ý tương đồng.
- **Online (Virtual Rooms)**: Phòng học ảo với tính năng gõ cửa xin vào và video call tích hợp **LiveKit WebRTC**.
- **Tech Stack**:
  - **Backend**: FastAPI (Python 3.11+), SQLite Async (`aiosqlite` + SQLAlchemy 2.0), In-Memory WebSocket Manager.
  - **Frontend**: Reflex (100% Python UI compile React).
  - **Video Call**: LiveKit Cloud WebRTC.
  - **AI Verification**: Google Gemini AI kiểm tra thẻ sinh viên tự động.

---

## 2. Create Environment (Tạo file .env)

Tạo file **`.env`** tại thư mục gốc dự án:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Các biến môi trường chính trong `.env`:
```env
DATABASE_URL=sqlite+aiosqlite:///./forfriend.db
JWT_SECRET_KEY=super-secret-key-forfriend-dev-only-change-in-prod

# LiveKit WebRTC (Video Call)
LIVEKIT_URL=wss://your-subdomain.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Google Gemini AI (Xác thực thẻ sinh viên)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash

# Cho phép truy cập mạng LAN
CORS_ORIGINS=["*"]
```

---

## 3. Quickstart (Khởi Chạy Nhanh)

### Cách 1: Khởi chạy 1-Click (Khuyên Dùng)

- **Windows**:
  ```cmd
  .\run_dev.bat
  ```
- **Linux / macOS**:
  ```bash
  chmod +x run_dev.sh && ./run_dev.sh
  ```

Địa chỉ truy cập:
- **Frontend Web**: `http://localhost:3000` (hoặc truy cập qua LAN: `http://<LAN_IP>:3000`)
- **Backend API & Swagger Docs**: `http://localhost:8000/docs`

---

### Cách 2: Khởi chạy thủ công

```bash
# 1. Tạo & kích hoạt virtual environment
python -m venv .venv
# Windows: .\.venv\Scripts\activate | Linux/macOS: source .venv/bin/activate

# 2. Cài đặt thư viện
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 3. Khởi tạo dữ liệu mẫu
python -m backend.app.init_db

# 4. Chạy Backend (Terminal 1)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Chạy Frontend (Terminal 2)
cd frontend && reflex run
```

---

### Tài Khoản Demo
| Email | Mật khẩu | Trường | Chuyên ngành / Lĩnh vực |
|:---|:---|:---|:---|
| `nguyenvana@ftu.edu.vn` | `Password123!` | ĐH Ngoại Thương Hà Nội | CNTT & Toán |
| `tranthib@neu.edu.vn` | `Password123!` | ĐH Kinh tế Quốc dân | Kinh tế & Ngoại ngữ |
