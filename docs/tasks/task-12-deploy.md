# Task 12 — Đóng Gói Nộp Đồ Án, Run Scripts & Kịch Bản Demo

## Mục tiêu
Chuẩn bị gói nộp đồ án môn học hoàn chỉnh đạt điểm tối đa:
- Tạo kịch bản khởi chạy tự động 1 click: `run_dev.bat` (Windows) và `run_dev.sh` (Linux / macOS).
- Soạn thảo tài liệu `README.md` nộp bài chi tiết, rõ ràng cho giảng viên/người chấm bài (cài đặt siêu nhanh, không cần cấu hình phức tạp, 0% Docker).
- Xây dựng kịch bản demo chấm điểm theo đầy đủ tính năng: Đăng ký (avatar chibi) → Bảng tin tìm bạn học (matching) → Tạo phòng học & Video Call → Đánh giá bạn học → Kết bạn & Nhắn tin riêng.
- Chuẩn hóa hướng dẫn đóng gói mã nguồn (loại bỏ virtualenv, file rác, dữ liệu tạm).

## Phụ thuộc
- Tất cả các tasks từ 01 đến 11 đã hoàn thành

---

## Yêu cầu chi tiết

### 12.1. File Chạy Nhanh Đồ Án (One-Click Run Scripts)

#### 1. Script cho Windows: `run_dev.bat` (Đặt tại thư mục gốc của project)
```bat
@echo off
chcp 65001 >nul
echo ===================================================================
echo     FORFRIEND — NỀN TẢNG TÌM BẠN HỌC (COURSE PROJECT DEMO)
echo          100%% Pure Python Stack — Zero External Services
echo ===================================================================

echo [1/3] Kiểm tra môi trường Backend...
if not exist "backend\.venv" (
    echo Chưa tìm thấy venv backend. Đang tạo .venv và cài đặt dependencies...
    cd backend
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
    python -m app.init_db
    cd ..
)

echo [2/3] Kiểm tra môi trường Frontend...
if not exist "frontend\.venv" (
    echo Chưa tìm thấy venv frontend. Đang tạo .venv và cài đặt dependencies...
    cd frontend
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
)

echo [3/3] Khởi động đồng thời Backend và Frontend...
start "ForFriend Backend [Port 8000]" cmd /k "cd backend && call .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"
timeout /t 3 >nul
start "ForFriend Frontend [Port 3000]" cmd /k "cd frontend && call .venv\Scripts\activate && reflex run"

echo.
echo ===================================================================
echo  Hệ thống đã sẵn sàng:
echo    - Trang chủ (Frontend):    http://localhost:3000
echo    - Tài liệu API (Swagger):  http://localhost:8000/docs
echo    - Database SQLite:         backend\forfriend.db (Tự sinh)
echo ===================================================================
pause
```

#### 2. Script cho Linux / macOS: `run_dev.sh` (Đặt tại thư mục gốc của project)
```bash
#!/usr/bin/env bash
set -e

echo "==================================================================="
echo "    FORFRIEND — NỀN TẢNG TÌM BẠN HỌC (COURSE PROJECT DEMO)"
echo "         100% Pure Python Stack — Zero External Services"
echo "==================================================================="

# 1. Backend venv check
if [ ! -d "backend/.venv" ]; then
    echo "[1/3] Khởi tạo môi trường Backend..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m app.init_db
    cd ..
fi

# 2. Frontend venv check
if [ ! -d "frontend/.venv" ]; then
    echo "[2/3] Khởi tạo môi trường Frontend..."
    cd frontend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 3. Start services
echo "[3/3] Khởi động đồng thời Backend và Frontend..."
(cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000) &
BE_PID=$!

sleep 3

(cd frontend && source .venv/bin/activate && reflex run) &
FE_PID=$!

trap "kill $BE_PID $FE_PID" EXIT

echo "==================================================================="
echo " Hệ thống đã sẵn sàng:"
echo "   - Trang chủ (Frontend):    http://localhost:3000"
echo "   - Tài liệu API (Swagger):  http://localhost:8000/docs"
echo "==================================================================="

wait
```

---

### 12.2. File Cấu Hình Môi Trường Mẫu (`.env.example`)

File `.env.example` đặt tại thư mục gốc và thư mục `backend/.env.example`:

```bash
# ==========================================
# CẤU HÌNH FORFRIEND (COURSE PROJECT)
# ==========================================

# 1. Database SQLite thuần Python (lưu trong backend/forfriend.db)
DATABASE_URL=sqlite+aiosqlite:///./forfriend.db

# 2. Security & JWT Token
JWT_SECRET_KEY=forfriend_super_secret_jwt_key_course_project_2026
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# 3. LiveKit Cloud (Tùy chọn cho Video Call - Đăng ký miễn phí tại cloud.livekit.io)
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_URL=wss://forfriend-demo.livekit.cloud

# 4. Storage & Uploads
UPLOAD_DIR=./uploads

# 5. CORS Allow
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

---

### 12.3. Cấu Trúc File `README.md` Dành Cho Giảng Viên / Người Chấm Bài

File `README.md` ở root phải có cấu trúc chuyên nghiệp, hướng dẫn từng bước:

```markdown
# ForFriend — Nền Tảng Tìm Bạn Học Nhóm Sinh Viên
> **Đồ án môn học**: Course Project
> **Phong cách**: Retro Game Pixel Art (Dark Theme Neon)
> **Kiến trúc**: 100% Pure Python Stack (Zero External Dependencies)

---

## ⚡ Khởi Chạy Nhanh Trong 2 Bước (Không Cần Cài Server Ngoài)

### Yêu cầu tiên quyết:
- Máy tính đã cài **Python 3.11+** (Khuyên dùng Python 3.11 hoặc 3.12).
- **KHÔNG CẦN** Docker, PostgreSQL hay Redis.

### Cách 1: Chạy 1 click (Khuyên dùng)
- **Trên Windows**: Nhấp đúp chuột vào file `run_dev.bat`.
- **Trên Linux / macOS**: Chạy lệnh `./run_dev.sh` trong Terminal.

### Cách 2: Chạy thủ công từng Terminal

#### Terminal 1 — Backend (FastAPI):
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows (hoặc source .venv/bin/activate trên Linux)
pip install -r requirements.txt
python -m app.init_db        # Tự động tạo file forfriend.db và nạp dữ liệu mẫu
uvicorn app.main:app --reload --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`

#### Terminal 2 — Frontend (Reflex):
```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate      # Windows (hoặc source .venv/bin/activate trên Linux)
pip install -r requirements.txt
reflex run
```
- Trang Web: `http://localhost:3000`
```

---

### 12.4. Kịch Bản Demo Chấm Điểm (Grading Demo Flow)

| Bước | Hành động demo | Kết quả mong đợi |
|:---:|:---|:---|
| **1** | Mở `http://localhost:3000`, bấm **"Start Quest"** | Màn hình đăng ký phong cách game xuất hiện |
| **2** | Điền thông tin sinh viên, chọn 1 trong **15 Avatar Chibi** | Tạo tài khoản thành công, tự động chuyển vào Dashboard |
| **3** | Mở tab **"Quest Board" (Bảng tin)** | Hiển thị danh sách bài đăng tìm bạn học offline được sắp xếp theo điểm tương đồng matching (cùng trường, khu vực, môn học) |
| **4** | Đăng một bài tìm bạn học mới | Bài đăng xuất hiện ngay trên bảng tin, cache feed in-memory tự động invalidate |
| **5** | Mở tab **"Adventure Zones" (Phòng học ảo)** | Hiển thị các khu vực học tập theo chủ đề (Toán học, Lập trình, Ngoại ngữ...) |
| **6** | User 2 xin vào phòng, Host duyệt | WebSocket in-memory phát tín hiệu real-time, cả 2 vào phòng học video WebRTC |
| **7** | Rời phòng học | Popup đánh giá 1–5 sao hiển thị, cập nhật uy tín người bạn học vào SQLite |
| **8** | Mở khung Chat 1-1 với bạn bè | Tin nhắn gửi nhận tức thì qua In-Memory WebSocket Manager kèm trạng thái online |

---

### 12.5. Hướng Dẫn Đóng Gói File Nộp Bài (.zip)

Trước khi nén file zip nộp bài, cần dọn dẹp các thư mục rác để giảm dung lượng file nộp (từ hàng trăm MB xuống còn dưới 15MB):

```bash
# Xóa môi trường ảo và cache build (người chấm bài sẽ tự tạo lại bằng 1 lệnh):
# 1. Xóa thư mục .venv trong backend/ và frontend/
# 2. Xóa thư mục frontend/.web (cache compile của Reflex)
# 3. Xóa các thư mục __pycache__ và .pytest_cache
# 4. Giữ lại file backend/forfriend.db (hoặc để script tự tạo mới)
```

File `.gitignore` chuẩn cho gói nộp:
```gitignore
# Virtual environments
.venv/
env/
venv/

# Python cache
__pycache__/
*.py[cod]
.pytest_cache/

# Reflex build output
frontend/.web/
frontend/.reflex/

# Uploads tạm
backend/uploads/*
!backend/uploads/.gitkeep

# OS files
.DS_Store
Thumbs.db
```

---

## Tiêu chí hoàn thành (Acceptance Criteria)

- [ ] File `run_dev.bat` và `run_dev.sh` hoạt động mượt mà, khởi động cả 2 server chỉ với 1 thao tác
- [ ] File `README.md` ở thư mục gốc hoàn chỉnh, trình bày đẹp mắt, hướng dẫn rõ ràng
- [ ] File `.env.example` đầy đủ các biến môi trường cần thiết
- [ ] Không còn bất kỳ file `Dockerfile` hay `docker-compose*.yml` nào trong mã nguồn
- [ ] Toàn bộ kịch bản demo chạy trơn tru, không gặp lỗi crash hoặc thiếu thư viện
