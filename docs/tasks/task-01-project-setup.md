# Task 01 — Project Setup & Infrastructure

## Mục tiêu
Khởi tạo project skeleton cho cả Backend (FastAPI) và Frontend (Reflex — Python-first), cấu hình Docker Compose với PostgreSQL + Redis, và đảm bảo mọi thứ chạy được với `docker-compose up`.

## Phụ thuộc
- Không có (task đầu tiên)

## Yêu cầu chi tiết

### 1.1. Backend Setup (FastAPI)

Tạo cấu trúc thư mục:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance, CORS, lifespan
│   ├── config.py             # Settings class (pydantic-settings)
│   ├── database.py           # Async SQLAlchemy engine + session
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── routers/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   └── websockets/
│       └── __init__.py
├── alembic/
│   └── (alembic init output)
├── alembic.ini
├── tests/
│   ├── __init__.py
│   └── test_health.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

**`requirements.txt`**:
```
fastapi==0.115.*
uvicorn[standard]==0.30.*
sqlalchemy[asyncio]==2.0.*
asyncpg==0.30.*
alembic==1.14.*
pydantic==2.*
pydantic-settings==2.*
python-jose[cryptography]==3.3.*
passlib[bcrypt]==1.7.*
python-multipart==0.0.*
redis==5.*
livekit-api==0.7.*
slowapi==0.1.*
bleach==6.*
httpx==0.27.*
pytest==8.*
pytest-asyncio==0.24.*
```

**`app/config.py`** — Dùng `pydantic-settings` để load từ `.env`:
```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/studybuddy"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # LiveKit
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    LIVEKIT_URL: str = "wss://your-app.livekit.cloud"
    
    # Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024     # 5MB
    MAX_CV_SIZE: int = 10 * 1024 * 1024        # 10MB
    
    # CORS — Reflex chạy trên port 3000
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    model_config = SettingsConfigDict(env_file=".env")
```

**`app/main.py`** — Phải có:
- CORS middleware
- Health check endpoint: `GET /health` → `{"status": "ok", "version": "0.1.0"}`
- Lifespan handler để init/close DB connections
- Include future routers

**`app/database.py`** — Async SQLAlchemy setup:
- `AsyncEngine` + `async_sessionmaker`
- `get_db()` dependency
- `Base = declarative_base()`

### 1.2. Frontend Setup (Reflex — Python-first)

Reflex là framework Python compile ra React. Không cần `npm` hay `node` — Reflex tự quản lý.

```bash
# Tạo và kích hoạt virtual env riêng cho frontend
cd frontend
python -m venv .venv
.venv\Scripts\activate  # Windows

pip install reflex==0.6.*  httpx==0.27.*

# Init Reflex app
reflex init
```

Cấu trúc thư mục:
```
frontend/
├── studybuddy/                  # Main app package
│   ├── __init__.py
│   ├── studybuddy.py            # App entry + routes
│   ├── pages/                   # Mỗi page là 1 file .py
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── register.py
│   │   └── dashboard.py
│   ├── components/              # Reusable UI components
│   │   └── __init__.py
│   ├── state/                   # Reflex State classes
│   │   ├── __init__.py
│   │   ├── auth_state.py
│   │   └── feed_state.py
│   ├── styles/                  # CSS variables + design tokens
│   │   └── theme.py             # Style dict dùng trong rx components
│   └── assets/                  # Avatars, sounds, icons
│       └── avatars/
├── rxconfig.py                  # Reflex config
├── requirements.txt             # Python deps
└── Dockerfile
```

**`rxconfig.py`** — Reflex cấu hình:
```python
import reflex as rx

config = rx.Config(
    app_name="studybuddy",
    api_url="http://localhost:8000",  # Backend FastAPI URL
    frontend_port=3000,
    backend_port=8001,               # Reflex backend (socket server)
)
```

**`studybuddy/studybuddy.py`** — Entry point và routing:
```python
import reflex as rx
from .pages import login, register, dashboard

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;500;600;700&display=swap",
    ],
)

app.add_page(login.login_page, route="/login")
app.add_page(register.register_page, route="/register")
app.add_page(dashboard.dashboard_page, route="/")
# ... more pages
```

**`requirements.txt`** (frontend):
```
reflex==0.6.*
httpx==0.27.*
```

### 1.3. Docker Compose

```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: studybuddy
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/studybuddy
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"   # Reflex frontend
      - "8001:8001"   # Reflex backend socket
    environment:
      API_URL: http://backend:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/.web          # Reflex build cache
    command: reflex run --env dev

volumes:
  pgdata:
```

### 1.4. Các file config khác
- `.env.example` ở root
- `backend/Dockerfile` (Python 3.11-slim)
- `frontend/Dockerfile` (Python 3.11-slim — chạy Reflex)
- `.gitignore` (thêm `.web/`, `.reflex/`)

## Tiêu chí hoàn thành (Acceptance Criteria)

- [ ] `docker-compose up` chạy thành công, không lỗi
- [ ] `GET http://localhost:8000/health` trả `{"status": "ok"}`
- [ ] `http://localhost:3000` hiển thị trang Reflex mặc định
- [ ] Frontend có thể gọi API backend qua `httpx` (đường dẫn `http://backend:8000/api/...`)
- [ ] Database PostgreSQL kết nối được từ backend
- [ ] Alembic init xong, chạy được `alembic upgrade head` (dù chưa có migration)
- [ ] `pytest` chạy pass test health check
- [ ] Reflex compile thành công (không lỗi khi `reflex run`)
