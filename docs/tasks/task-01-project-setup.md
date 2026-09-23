# Task 01 — Project Setup & Pure Python Infrastructure

## Mục tiêu
Khởi tạo project skeleton cho cả Backend (FastAPI) và Frontend (Reflex — Python-first), cấu hình Python virtual environment (`.venv`), kết nối SQLite 3 async (`aiosqlite`), và đảm bảo hệ thống chạy trực tiếp bằng lệnh Python thuần mà **không cần cài đặt Docker, PostgreSQL hay Redis**.

## Phụ thuộc
- Không có (task đầu tiên)

## Yêu cầu chi tiết

### 1.1. Backend Setup (FastAPI + SQLite)

Tạo cấu trúc thư mục backend:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance, CORS, lifespan (auto create DB)
│   ├── config.py             # Settings class (pydantic-settings, load from .env)
│   ├── database.py           # Async SQLite engine (sqlite+aiosqlite:///./forfriend.db)
│   ├── init_db.py            # Script tạo bảng & nạp seed categories
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── routers/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── memory_cache.py   # In-Memory Cache với TTL
│   └── websockets/
│       ├── __init__.py
│       └── connection_manager.py # In-Memory WebSocket Manager
├── tests/
│   ├── __init__.py
│   └── test_health.py
├── requirements.txt
├── .env.example
└── forfriend.db              # Tự sinh khi server khởi chạy
```

**`backend/requirements.txt`**:
```
fastapi==0.115.*
uvicorn[standard]==0.30.*
sqlalchemy[asyncio]==2.0.*
aiosqlite==0.20.*
pydantic==2.*
pydantic-settings==2.*
python-jose[cryptography]==3.3.*
passlib[bcrypt]==1.7.*
python-multipart==0.0.*
livekit-api==0.7.*
slowapi==0.1.*
bleach==6.*
httpx==0.27.*
pytest==8.*
pytest-asyncio==0.24.*
```

**`backend/app/config.py`** — Dùng `pydantic-settings` load từ `.env`:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database SQLite thuần Python (lưu tại thư mục backend/)
    DATABASE_URL: str = "sqlite+aiosqlite:///./forfriend.db"
    
    # JWT
    JWT_SECRET_KEY: str = "super-secret-key-forfriend-dev-only-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # LiveKit (Cloud Free Tier)
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    LIVEKIT_URL: str = "wss://your-app.livekit.cloud"
    
    # Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024     # 5MB
    MAX_CV_SIZE: int = 10 * 1024 * 1024        # 10MB
    
    # CORS — Frontend Reflex mặc định port 3000
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
```

**`backend/app/database.py`** — Async SQLite setup:
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},  # Cần cho SQLite
)

# Bật Foreign Key check cho SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

**`backend/app/main.py`** — Khởi chạy & Tự động tạo bảng:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
import app.models  # Nạp toàn bộ models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo bảng tự động khi start server (tiện cho đồ án)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="ForFriend API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0", "database": "sqlite"}
```

---

### 1.2. Frontend Setup (Reflex — Python-first)

Reflex biên dịch Python sang React hoàn toàn tự động trong thư mục `.web/`:

```bash
# Tạo môi trường cho Frontend
cd frontend
python -m venv .venv
# Kích hoạt venv (Windows: .venv\Scripts\activate, Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt

# Khởi tạo project Reflex
reflex init
```

Cấu trúc thư mục frontend:
```
frontend/
├── forfriend/                  # Main package Reflex
│   ├── __init__.py
│   ├── forfriend.py            # App entry point + routes registry
│   ├── pages/                  # Mỗi trang là 1 module Python
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── register.py
│   │   └── dashboard.py
│   ├── components/             # Reusable UI components
│   │   ├── __init__.py
│   │   └── livekit_component.py # Wrap WebRTC video
│   ├── state/                  # Reflex State classes
│   │   ├── __init__.py
│   │   ├── auth_state.py
│   │   └── feed_state.py
│   ├── styles/                 # Design tokens phong cách retro game
│   │   └── theme.py
│   └── assets/                 # 15 avatar chibi, icons, sound fx
│       └── avatars/
├── rxconfig.py                 # Cấu hình Reflex
└── requirements.txt            # reflex, httpx...
```

**`frontend/requirements.txt`**:
```
reflex==0.6.*
httpx==0.27.*
```

**`frontend/rxconfig.py`**:
```python
import reflex as rx

config = rx.Config(
    app_name="forfriend",
    api_url="http://localhost:8000",   # Địa chỉ FastAPI Backend
    frontend_port=3000,
    backend_port=8001,
)
```

---

### 1.3. Khởi Chạy Local Trực Tiếp (Zero Docker)

Toàn bộ dự án chạy trực tiếp trên máy thông qua 2 terminal riêng biệt hoặc dùng file script tiện lợi:

#### Terminal 1 — Backend:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Trên Windows
# source .venv/bin/activate     # Trên Linux / macOS
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API Documentation tự động mở tại: `http://localhost:8000/docs`

#### Terminal 2 — Frontend:
```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate          # Trên Windows
# source .venv/bin/activate     # Trên Linux / macOS
pip install -r requirements.txt
reflex run
```
Trang chủ tự động mở tại: `http://localhost:3000`

---

### 1.4. Script Chạy Nhanh 1-Click (Dành Cho Đồ Án)

Tạo file `run_dev.bat` tại thư mục gốc dự án (cho Windows):
```bat
@echo off
echo ==========================================
echo Starting ForFriend (Pure Python Edition)
echo ==========================================

start "ForFriend Backend" cmd /k "cd backend && call .venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"
timeout /t 3
start "ForFriend Frontend" cmd /k "cd frontend && call .venv\Scripts\activate && reflex run"

echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:3000
```

Tạo file `run_dev.sh` tại thư mục gốc dự án (cho Linux/macOS):
```bash
#!/bin/bash
echo "Starting ForFriend (Pure Python Edition)..."
(cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000) &
sleep 3
(cd frontend && source .venv/bin/activate && reflex run) &
wait
```

---

## Tiêu chí hoàn thành (Acceptance Criteria)

- [ ] Cài đặt dependencies thành công mà không yêu cầu Docker/Docker Compose
- [ ] Backend khởi động tại `http://localhost:8000`, `GET /health` trả về `{"status": "ok", "database": "sqlite"}`
- [ ] File SQLite `backend/forfriend.db` tự động được sinh khi server backend khởi chạy lần đầu
- [ ] Swagger UI tại `http://localhost:8000/docs` xem và thử nghiệm được bình thường
- [ ] Frontend Reflex biên dịch thành công và hiển thị tại `http://localhost:3000`
- [ ] `pytest tests/test_health.py` chạy thành công (100% pass)
- [ ] Không có bất kỳ phụ thuộc nào vào PostgreSQL server hay Redis server
