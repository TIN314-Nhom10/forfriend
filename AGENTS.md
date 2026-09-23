# AGENTS.md — Quy Định & Hướng Dẫn Dành Cho AI Agent (ForFriend)

> **Tài liệu hướng dẫn bắt buộc dành cho mọi AI Agent (Antigravity, Claude, Gemini, GPT, Cursor, etc.) khi tham gia đọc hiểu, bảo trì hoặc phát triển dự án ForFriend.**

---

## 1. Tổng Quan Dự Án (Project Mission)

- **Tên dự án**: ForFriend (Course Project / Đồ án sinh viên)
- **Mục tiêu**: Nền tảng web giúp sinh viên kết nối tìm bạn học nhóm — hỗ trợ cả **Offline** (bảng tin tìm bạn học theo trường/khu vực/môn học) lẫn **Online** (phòng học ảo kèm video call tích hợp).
- **Điểm nhấn cốt lõi**:
  1. **Phong cách Web Game Retro**: Dark theme neon (`#0a0a1a`), pixel font ("Press Start 2P"), hiệu ứng glow, terminology game hóa ("Quest", "Hero", "Zone", "Level/Rating").
  2. **15 Avatar Chibi có sẵn**: Người dùng chọn avatar đại diện theo phong cách pixel/chibi ngay khi đăng ký.
  3. **100% Pure Python Stack (Zero External Dependencies)**: 
     - **KHÔNG dùng Docker** (chạy trực tiếp bằng Python virtualenv).
     - **Database có sẵn trong Python**: SQLite (kết hợp `aiosqlite` cho async) lưu trong file `forfriend.db`.
     - **Cache & Pub/Sub in-memory**: Quản lý WebSocket và Cache thuần Python bằng `dict` và `asyncio.Queue` (thay thế Redis).
     - **Frontend**: Reflex (100% Python UI compile sang React).
     - **Backend**: FastAPI (Python 3.11+).

---

## 2. Tech Stack & Kiến Trúc Cốt Lõi

```
┌────────────────────────────────────────────────────────────────────────┐
│               FRONTEND: Reflex (Python → React Compile)                │
│  - 100% Python code cho Pages, Components, State Management            │
│  - Styling: Vanilla CSS Game Tokens (CSS Variables, KHÔNG dùng Tailwind)│
│  - Typography: "Press Start 2P" (Headings/Buttons) + "Inter" (Body)    │
│  - LiveKit Component: Reflex Custom Component JS Wrapper (~5% JS)      │
│  - HTTP/WS: Async httpx client + Reflex WebSocket Engine               │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST API + WebSocket (/api/v1/)
┌───────────────────────────────────▼────────────────────────────────────┐
│                    BACKEND: FastAPI (Python 3.11+)                     │
│  - Async REST API + Native WebSocket Handlers                          │
│  - ORM: SQLAlchemy 2.0 (Async Session) + aiosqlite                     │
│  - Data Validation: Pydantic v2                                        │
│  - Authentication: JWT (access + refresh tokens) + passlib/bcrypt      │
│  - Real-time Hub: In-Memory ConnectionManager (asyncio / dict)         │
│  - Matching Engine: Relevance scoring algorithm (School, City, Subject)│
│  - Media Service: LiveKit Server SDK (Generate room access tokens)     │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
┌──────────────────▼───────────────┐ ┌───────────────▼───────────────────┐
│      DATABASE: SQLite 3          │ │   CACHE & PUB/SUB: In-Memory RAM  │
│  - File: `forfriend.db`         │ │  - WebSocket ConnectionManager    │
│  - 10 Bảng (Users, Posts, etc.)  │ │  - Memory Dict Cache (with TTL)   │
│  - Không cần cài server ngoài    │ │  - 0% phụ thuộc Redis/Docker      │
└──────────────────────────────────┘ └───────────────────────────────────┘
```

---

## 3. Cấu Trúc Thư Mục Dự Án (Project Layout)

Agent tuân thủ cấu trúc gọn gàng, không cần Docker:

```
side-python-prj/
├── AGENTS.md                          # Tài liệu này (hướng dẫn cho Agent)
├── req.txt                            # Yêu cầu tính năng gốc của khách hàng
├── overview.pdf                       # Bản thiết kế/yêu cầu ban đầu
├── .env.example                       # Mẫu cấu hình môi trường chuẩn
│
├── docs/                              # Toàn bộ tài liệu kỹ thuật chi tiết
│   ├── 00-overview.md                 # Tổng quan dự án, tech stack, conventions
│   ├── 01-architecture.md             # Sơ đồ kiến trúc & luồng dữ liệu (Mermaid)
│   ├── 02-database-schema.md          # Chi tiết 10 bảng, quan hệ, SQLite schema
│   ├── 03-api-design.md               # Đặc tả toàn bộ REST endpoints & WebSocket events
│   ├── tasks/                         # 12 tài liệu hướng dẫn triển khai từng task
│   └── prompts/                       # Reference prompts cho từng role
│
├── backend/                           # FastAPI Service (Python)
│   ├── app/
│   │   ├── main.py                    # Entry point, router mount, lifespan
│   │   ├── config.py                  # Pydantic Settings load từ .env
│   │   ├── database.py                # Async SQLite engine (sqlite+aiosqlite:///./forfriend.db)
│   │   ├── models/                    # SQLAlchemy async models
│   │   ├── schemas/                   # Pydantic request/response schemas
│   │   ├── routers/                   # Endpoint handlers (/api/v1/...)
│   │   ├── services/                  # Business logic & DB transactions
│   │   ├── utils/                     # Security, token, matching, sanitizer
│   │   └── websockets/                # In-memory ConnectionManager & handlers
│   ├── tests/                         # Pytest test suites
│   ├── requirements.txt               # fastapi, uvicorn, sqlalchemy, aiosqlite, etc.
│   └── forfriend.db                  # File database SQLite (tự sinh khi chạy)
│
└── frontend/                          # Reflex App (Python-first UI)
    ├── rxconfig.py                    # Cấu hình Reflex app
    ├── requirements.txt               # reflex, httpx, etc.
    ├── ForFriend/
    │   ├── ForFriend.py              # Reflex main app & route registry
    │   ├── state/                     # Reflex State classes (Auth, Feed, Room...)
    │   ├── pages/                     # Các trang: Login, Feed, Lobby, Call, Chat...
    │   ├── components/                # Reusable game components (Navbar, Cards...)
    │   │   └── livekit_component.py   # Reflex Custom Component wrapper cho WebRTC
    │   ├── styles/                    # Design tokens & styles.css
    │   └── assets/                    # 15 chibi avatars, pixel art icons, sounds
```

---

## 4. Nguyên Tắc Hoạt Động Của AI Agent (Operating Protocols)

### 4.1. Quy trình làm việc: Đọc trước — Lập kế hoạch — Thực thi — Kiểm thử
1. **BẮT BUỘC ĐỌC TÀI LIỆU LIÊN QUAN TRƯỚC KHI CODE**:
   - Khi làm bất kỳ task nào, Agent **phải đọc** file `docs/tasks/task-XX-*.md` tương ứng.
   - Đối chiếu với `docs/02-database-schema.md` khi thao tác bảng dữ liệu.
   - Đối chiếu với `docs/03-api-design.md` khi tạo hoặc gọi endpoint API.
2. **Tuân thủ thứ tự ưu tiên các tầng (Layer Priority)**:
   - **Backend**: `Model` → `Schema` → `Service` → `Router` → `Test`.
   - **Frontend**: `State` → `API Service` → `Component` → `Page` → `Style`.
3. **Môi trường chạy**:
   - Dùng Python virtualenv (`.venv`). Tuyệt đối **không yêu cầu hay phụ thuộc vào Docker/Docker Compose**.
   - Chạy Backend: `uvicorn app.main:app --reload --port 8000`
   - Chạy Frontend: `reflex run`
4. **Kiểm tra và tự xác minh (Verification)**:
   - Backend: Viết test với `pytest` + `pytest-asyncio`.
   - Frontend: Kiểm tra code compile sạch với `reflex run`, không có exception cú pháp.
5. **Quy ước Git**:
   - Branch: `feature/task-XX-ten-task` hoặc `fix/mo-ta-loi`.
   - Commit: Tuân thủ Conventional Commits (ví dụ: `feat(auth): implement JWT login flow`).

---

## 5. Quy Chuẩn Kỹ Thuật Chi Tiết (Coding Standards)

### 5.1. Backend (FastAPI, SQLite & In-Memory Hub)
- **Async Everywhere**: Dùng `async` / `await` cho DB queries (`aiosqlite`), HTTP request (`httpx`) và WebSocket.
- **Database (SQLite)**:
  - Connection URL: `sqlite+aiosqlite:///./forfriend.db`
  - Khóa chính: String UUID (`str(uuid.uuid4())`) hoặc Integer Auto-increment (khuyến nghị UUID string).
  - Tên bảng: `snake_case` số ít (`user`, `post`, `room`, `message`...).
  - Tự động tạo bảng khi khởi động app bằng `Base.metadata.create_all(engine)` trong lifespan event của FastAPI (hoặc Alembic migration nếu cần).
- **Real-time & Cache (In-Memory)**:
  - Dùng `ConnectionManager` class lưu trữ `dict[str, WebSocket]` để broadcast/gửi tin nhắn WebSocket.
  - Cache tính toán matching / session lưu bằng Python `dict` có timestamp (TTL). Không dùng Redis server.
- **Kiến trúc 3 lớp (3-Tier)**:
  - `routers/`: Chỉ parse request, validate schema, gọi service, trả HTTP response.
  - `services/`: Chứa business logic, xử lý dữ liệu và transaction DB.
  - `models/`: Định nghĩa thực thể SQLAlchemy.
- **Data Validation & Sanitization**:
  - Dùng Pydantic v2 với type annotation chặt chẽ.
  - Dùng `bleach` để sanitize text input người dùng chống XSS.
- **Security & Secrets**:
  - Hash mật khẩu bằng `passlib.context.CryptContext` (bcrypt).
  - Load biến môi trường từ file `.env` qua `pydantic-settings`.
- **Logging**:
  - Dùng module `logging` chuẩn của Python. Không dùng `print()` trong code service/router.

### 5.2. Frontend (Reflex — Python-first)
- **Triết lý Python-first**:
  - Toàn bộ giao diện, router, state management được viết bằng Python thông qua thư viện Reflex.
  - Mỗi trang là một Python module trả về component (ví dụ: `def feed_page() -> rx.Component:`).
- **Quản lý State (`rx.State`)**:
  - Tổ chức state theo module chức năng (`AuthState`, `FeedState`, `RoomState`, `ChatState`).
  - Biến state có type hints rõ ràng. Event handlers là method của class kế thừa từ `rx.State`.
- **Styling & Design System**:
  - **KHÔNG dùng Tailwind CSS**.
  - Sử dụng hệ thống CSS Variables định nghĩa trong `frontend/ForFriend/styles/index.css`.
- **Ngoại lệ JavaScript duy nhất (~5%)**:
  - Video Call WebRTC qua LiveKit Cloud: Dùng Reflex Custom Component (`rx.Component`) wrap LiveKit React SDK trong `livekit_component.py`.

### 5.3. Design System: Phong Cách Web Game Retro
Agent phải giữ vững tính thẩm mỹ game xuyên suốt mọi màn hình:
1. **Màu sắc cốt lõi**:
   - Nền chính: Dark Space `#0a0a1a` hoặc `#0f0f23`
   - Nền Card/Panel: `#16162e` hoặc `#1b1b3a`
   - Màu nhấn chủ đạo: **Neon Green** `#00ff88`
   - Màu phụ: **Neon Pink** `#ff007f`, **Cyan Glow** `#00e5ff`, **Retro Gold** `#ffe600`
2. **Typography**:
   - Tiêu đề, nút bấm, nhãn chỉ số: Font **"Press Start 2P"** (pixel font).
   - Nội dung dài, đoạn văn, tin nhắn: Font **"Inter"** hoặc sans-serif sạch.
3. **Hiệu ứng & Visual**:
   - Pixel art border (box-shadow retro `2px 2px 0px #000, 4px 4px 0px var(--neon-color)`).
   - Micro-animations: Floating avatar, pulse badge.
4. **Thuật ngữ game hóa (Gamification Language)**:
   - Bài tìm bạn học ➔ *Quest / Mission*
   - Hồ sơ người dùng ➔ *Hero Profile* (kèm EXP, Level, Star Rating)
   - Khu vực phòng học ➔ *Adventure Zones*
   - 15 Avatar Chibi: Cung cấp sẵn file ảnh tại `frontend/ForFriend/assets/avatars/`.

---

## 6. Lộ Trình Triển Khai 12 Tasks (Roadmap - No Docker Edition)

| Task | Tên Task | Trọng tâm thực hiện |
|:---:|:---|:---|
| **01** | Project Setup | Khởi tạo venv, cài đặt dependencies, setup FastAPI + Reflex skeleton |
| **02** | Database Models | 10 Models SQLAlchemy (SQLite compatible), script tạo tables & seed data mẫu |
| **03** | Auth System | Register (kèm avatar), Login, JWT Auth, Password Hash |
| **04** | User Profile | Xem/Sửa Profile, Upload ảnh thẻ SV & CV (local storage), Đổi Avatar |
| **05** | Post Feed | CRUD bài đăng tìm bạn học offline, phân trang, lọc theo trường/môn |
| **06** | Matching Algorithm | Tính điểm tương đồng (School 40%, Location 30%, Subject 30%), In-memory cache |
| **07** | Room System | Tạo phòng học ảo, Lobby phân khu, In-memory WebSocket xin vào / duyệt |
| **08** | Video Call LiveKit | Tích hợp LiveKit Server SDK cấp token, Custom Component Reflex hiển thị video |
| **09** | Rating System | Đánh giá 1–5 sao sau khi rời phòng, tính điểm uy tín |
| **10** | Friend & Chat | Kết bạn, danh sách bạn bè, Chat 1-1 qua In-memory WebSocket ConnectionManager |
| **11** | Frontend Game UI | Xây dựng toàn bộ giao diện Reflex: Pixel components, trang, CSS tokens |
| **12** | Local Run & Demo | Viết script run dự án (.bat/.sh), README hướng dẫn nộp đồ án môn học |

---

## 7. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

1. **Khởi chạy trực tiếp, 0 lỗi**: Chạy được cả Backend và Frontend trực tiếp bằng lệnh Python trên máy, không đòi hỏi cài đặt Docker, PostgreSQL hay Redis.
2. **Database SQLite tự sinh**: File `forfriend.db` tự khởi tạo với đầy đủ 10 bảng và dữ liệu mẫu khi start server lần đầu.
3. **API Specification**: Đầy đủ endpoint theo đúng `docs/03-api-design.md`, Swagger UI tại `http://localhost:8000/docs` test được bình thường.
4. **Real-time hoạt động**: Chat 1-1 và Duyệt vào phòng hoạt động real-time thông qua In-Memory WebSocket Manager.
5. **Trải nghiệm Game UI**: Giao diện dark mode retro game mượt mà, đúng chuẩn pixel art.

---

> *Agent Note*: Khi triển khai, ưu tiên giải pháp gọn nhẹ nhất, code sạch, có type hints và tận dụng tối đa thư viện có sẵn trong Python ecosystem.
