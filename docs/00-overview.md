# forfriend — Tổng Quan Dự Án

## 1. Tầm nhìn (Vision)

**forfriend** là nền tảng web giúp sinh viên tìm bạn học cùng — cả online (video call) lẫn offline (đi học nhóm). Giao diện mang phong cách **game retro / pixel art** với avatar chibi, tạo cảm giác thú vị và khác biệt so với các ứng dụng học tập truyền thống.

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

## 3. Tech Stack (100% Pure Python Stack)

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│  Reflex (Python → React compile) ← Python-first!   │
│  CSS: Vanilla CSS (Game-style design system tokens) │
│  Font: "Press Start 2P" (Google Fonts) + "Inter"    │
│  Icons: Pixel-art custom SVG                        │
│  Video Call: LiveKit React SDK (wrap qua Reflex     │
│              Custom Component — ngoại lệ duy nhất)  │
│  Real-time: Reflex State + native WebSocket         │
└──────────────────────┬──────────────────────────────┘
                       │ REST API + WebSocket (/api/v1/)
┌──────────────────────▼──────────────────────────────┐
│                    BACKEND                          │
│  Python 3.11+ / FastAPI                             │
│  ORM: SQLAlchemy 2.0 (async mode với aiosqlite)     │
│  Auth: JWT (python-jose) + bcrypt (passlib)         │
│  Validation: Pydantic v2                            │
│  Real-time Hub: FastAPI native WebSocket +         │
│                 In-Memory ConnectionManager         │
│  Matching Engine: Thuật toán tính độ phù hợp        │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│             DATA & IN-MEMORY LAYER                  │
│  Database: SQLite 3 (file `forfriend.db` qua        │
│            aiosqlite async driver)                  │
│  Cache & Pub-Sub: In-Memory Python RAM              │
│                   (Memory dict có TTL + Queue)      │
│  Video SFU: LiveKit Cloud (Free tier WebRTC)        │
│  File Storage: Local disk (thư mục `./uploads`)     │
│  Môi trường: Python virtualenv (.venv) — 0% Docker │
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
│   │   ├── database.py            # SQLite async engine (sqlite+aiosqlite:///./forfriend.db)
│   │   ├── init_db.py             # Script tự động tạo bảng & seed categories
│   │   ├── models/                # SQLAlchemy models (10 tables)
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── routers/               # API route handlers
│   │   ├── services/              # Business logic
│   │   ├── utils/                 # Helpers (auth, matching, in-memory cache...)
│   │   └── websockets/            # In-Memory ConnectionManager & WS handlers
│   ├── tests/
│   ├── requirements.txt           # fastapi, uvicorn, sqlalchemy, aiosqlite...
│   └── forfriend.db               # File database SQLite (tự sinh khi khởi động)
│
├── frontend/                      # Reflex app (Python-first UI)
│   ├── forfriend/                 # Reflex app package
│   │   ├── forfriend.py           # App entry point & routes
│   │   ├── pages/                 # Python pages
│   │   ├── components/            # Python components
│   │   │   └── livekit_component.py # Wrap WebRTC LiveKit
│   │   ├── state/                 # Reflex State classes
│   │   ├── styles/                # CSS variables + game design tokens
│   │   └── assets/                # 15 chibi avatars, pixel art icons, sounds
│   ├── rxconfig.py                # Reflex config
│   └── requirements.txt           # reflex, httpx...
│
├── run_dev.bat                    # Script chạy nhanh cả 2 server trên Windows
├── run_dev.sh                     # Script chạy nhanh cả 2 server trên Linux/macOS
├── .env.example
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
