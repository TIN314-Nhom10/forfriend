# StudyBuddy — Tổng Quan Dự Án

## 1. Tầm nhìn (Vision)

**StudyBuddy** là nền tảng web giúp sinh viên tìm bạn học cùng — cả online (video call) lẫn offline (đi học nhóm). Giao diện mang phong cách **game retro / pixel art** với avatar chibi, tạo cảm giác thú vị và khác biệt so với các ứng dụng học tập truyền thống.

---

## 2. Danh sách tính năng chính

| # | Tính năng | Mô tả ngắn |
|---|-----------|-------------|
| F1 | **Đăng ký / Đăng nhập** | Tạo tài khoản với thông tin: Tên, Năm sinh, Ngành, Trường, Địa chỉ, Thẻ sinh viên, CV. Chọn 1 trong 15 avatar chibi. |
| F2 | **Bảng tin (Feed)** | Khu vực đăng bài tìm bạn học offline (như Facebook). Thuật toán matching đẩy bài đến người có điểm chung (cùng trường, khu vực, môn học). |
| F3 | **Phòng học Online** | Tạo phòng video call giống Google Meet / Zoom. Người khác gửi request xin vào, host duyệt. |
| F4 | **Phân loại phòng theo chủ đề** | Phòng có tag chủ đề. Các phòng cùng chủ đề được gom thành "khu vực" trên bản đồ/lobby. |
| F5 | **Đánh giá bạn học** | Sau khi rời phòng, đánh giá bạn học 1–5 sao. |
| F6 | **Kết bạn & Nhắn tin riêng** | Gửi lời mời kết bạn, nhắn tin 1-1 real-time. |
| F7 | **Giao diện Game-style** | UI phong cách web game: pixel art, retro border, animation, sound effects nhẹ. |
| F8 | **15 Avatar Chibi** | Bộ 15 avatar chibi có sẵn để người dùng chọn khi đăng ký / đổi trong profile. |

---

## 3. Tech Stack

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│  Reflex (Python → React)  ← Python-first!           │
│  CSS: Vanilla CSS (Game-style design system)        │
│  Font: "Press Start 2P" (Google Fonts)              │
│  Icons: Pixel-art custom SVG                        │
│  Video Call: LiveKit JS (wrap qua Reflex Custom     │
│              Component — ngoại lệ duy nhất ~5% JS)  │
│  Real-time: Reflex State + native WebSocket         │
└──────────────────────┬──────────────────────────────┘
                       │ REST API + WebSocket
┌──────────────────────▼──────────────────────────────┐
│                    BACKEND                          │
│  Python 3.11+ / FastAPI                             │
│  ORM: SQLAlchemy 2.0 (async)                        │
│  Auth: JWT (python-jose) + bcrypt                   │
│  Validation: Pydantic v2                            │
│  WebSocket: FastAPI native                          │
│  Task Queue: Celery + Redis (optional, cho email)   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                 INFRASTRUCTURE                      │
│  Database: PostgreSQL 15                            │
│  Cache / Pub-Sub: Redis 7                           │
│  Video SFU: LiveKit Cloud (Free tier)               │
│  File Storage: Local disk (dev) / S3 (prod)         │
│  Containerization: Docker + docker-compose          │
└─────────────────────────────────────────────────────┘
```

---

## 4. Cấu trúc thư mục dự án (Target)

```
side-python-prj/
├── docs/                          # Tài liệu dự án (thư mục này)
│   ├── 00-overview.md
│   ├── 01-architecture.md
│   ├── 02-database-schema.md
│   ├── 03-api-design.md
│   ├── tasks/                     # Từng task chi tiết
│   │   ├── task-01-project-setup.md
│   │   ├── task-02-database-models.md
│   │   ├── task-03-auth-system.md
│   │   ├── task-04-user-profile.md
│   │   ├── task-05-post-feed.md
│   │   ├── task-06-matching-algorithm.md
│   │   ├── task-07-room-system.md
│   │   ├── task-08-video-call-livekit.md
│   │   ├── task-09-rating-system.md
│   │   ├── task-10-friend-chat.md
│   │   ├── task-11-frontend-game-ui.md
│   │   └── task-12-deploy.md
│   └── prompts/                   # Agent prompts cho từng role
│       ├── agent-backend.md
│       ├── agent-frontend.md
│       └── agent-fullstack.md
│
├── backend/                       # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── routers/               # API route handlers
│   │   ├── services/              # Business logic
│   │   ├── utils/                 # Helpers (auth, matching...)
│   │   └── websockets/            # WebSocket handlers
│   ├── alembic/                   # DB migrations
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                      # Reflex app (Python-first)
│   ├── studybuddy/                # Reflex app package
│   │   ├── studybuddy.py          # App entry point
│   │   ├── pages/                 # Python pages
│   │   ├── components/            # Python components
│   │   ├── state/                 # Reflex State classes
│   │   ├── styles/                # CSS variables + game design
│   │   └── assets/                # Avatars, pixel art, sounds
│   ├── rxconfig.py                # Reflex config
│   ├── requirements.txt           # Python deps (không có package.json)
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── req.txt                        # Yêu cầu gốc
└── README.md
```

---

## 5. Quy ước chung (Conventions)

### Naming
- **Python (Backend + Frontend)**: `snake_case` cho biến/hàm, `PascalCase` cho class
- **Reflex Components**: Python function hoặc class, `PascalCase` hoặc `snake_case` theo Reflex convention
- **Database**: `snake_case` cho table/column, table name số ít (`user`, `post`, `room`)
- **API URL**: `kebab-case`, prefix `/api/v1/`

### Git
- Branch: `feature/task-XX-ten-task`, `fix/mo-ta-ngan`
- Commit: `feat(scope): mô tả` theo Conventional Commits

### Code Quality
- Backend: type hints bắt buộc, docstring cho mọi function public
- Frontend (Reflex): type hints bắt buộc, docstring cho State class và component phức tạp
- Mỗi module phải có unit test cơ bản

### Environment Variables
- Dùng file `.env` + `pydantic-settings` để load config
- KHÔNG hardcode secret vào source code
