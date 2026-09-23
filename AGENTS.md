# AGENTS.md — Quy Định & Hướng Dẫn Dành Cho AI Agent (StudyBuddy)

> **Tài liệu hướng dẫn bắt buộc dành cho mọi AI Agent (Antigravity, Claude, Gemini, GPT, Cursor, etc.) khi tham gia đọc hiểu, bảo trì hoặc phát triển dự án StudyBuddy.**

---

## 1. Tổng Quan Dự Án (Project Mission)

- **Tên dự án**: StudyBuddy
- **Mục tiêu**: Nền tảng web giúp sinh viên kết nối tìm bạn học nhóm — hỗ trợ cả **Offline** (bảng tin tìm bạn học theo trường/khu vực/môn học) lẫn **Online** (phòng học ảo kèm video call tích hợp).
- **Điểm nhấn đặc biệt**:
  1. **Phong cách Web Game Retro**: Dark theme neon (`#0a0a1a`), pixel font ("Press Start 2P"), hiệu ứng glow, terminology game hóa ("Quest", "Hero", "Zone", "Level/Rating").
  2. **15 Avatar Chibi có sẵn**: Người dùng chọn avatar đại diện theo phong cách pixel/chibi ngay khi đăng ký.
  3. **Python-first Fullstack**: Tối ưu hóa tối đa việc dùng Python cho cả Backend (FastAPI) và Frontend (Reflex), hạn chế tối thiểu việc viết JavaScript/Node.js.

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
│  - ORM: SQLAlchemy 2.0 (Async Session) + asyncpg                       │
│  - Data Validation: Pydantic v2                                        │
│  - Authentication: JWT (access + refresh tokens) + passlib/bcrypt      │
│  - Matching Engine: Relevance scoring algorithm (School, City, Subject)│
│  - Media Service: LiveKit Server SDK (Generate room access tokens)     │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
┌──────────────────▼───────────────┐ ┌───────────────▼───────────────────┐
│     DATABASE: PostgreSQL 15      │ │      CACHE & PUB/SUB: Redis 7     │
│  - 10 Bảng (Users, Posts, Rooms, │ │  - Session & Feed Cache           │
│    Ratings, Messages, etc.)      │ │  - Real-time Pub/Sub (Chat & WS)  │
│  - Alembic migrations            │ │  - Rate Limiting                  │
└──────────────────────────────────┘ └───────────────────────────────────┘
```

---

## 3. Cấu Trúc Thư Mục Dự Án (Project Layout)

Agent phải tuân thủ nghiêm ngặt vị trí đặt file theo sơ đồ cấu trúc:

```
side-python-prj/
├── AGENTS.md                          # Tài liệu này (hướng dẫn cho Agent)
├── req.txt                            # Yêu cầu tính năng gốc của khách hàng
├── overview.pdf                       # Bản thiết kế/yêu cầu ban đầu
├── docker-compose.yml                 # Docker chạy PostgreSQL, Redis, Backend, Frontend
├── .env.example                       # Mẫu cấu hình môi trường chuẩn
│
├── docs/                              # Toàn bộ tài liệu kỹ thuật chi tiết
│   ├── 00-overview.md                 # Tổng quan dự án, tech stack, conventions
│   ├── 01-architecture.md             # Sơ đồ kiến trúc & luồng dữ liệu (Mermaid)
│   ├── 02-database-schema.md          # Chi tiết 10 bảng, quan hệ, indexes
│   ├── 03-api-design.md               # Đặc tả toàn bộ REST endpoints & WebSocket events
│   ├── tasks/                         # 12 tài liệu hướng dẫn triển khai từng task
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
│   └── prompts/                       # Reference prompts cho từng role
│
├── backend/                           # FastAPI Service (Python)
│   ├── app/
│   │   ├── main.py                    # Entry point, middleware, router mount
│   │   ├── config.py                  # Pydantic Settings load từ .env
│   │   ├── database.py                # Async engine & sessionmaker
│   │   ├── models/                    # SQLAlchemy async models
│   │   ├── schemas/                   # Pydantic request/response schemas
│   │   ├── routers/                   # Endpoint handlers (/api/v1/...)
│   │   ├── services/                  # Business logic & DB transactions
│   │   ├── utils/                     # Security, token, matching, sanitizer
│   │   └── websockets/                # WebSocket connection manager
│   ├── alembic/                       # DB migration scripts
│   ├── tests/                         # Pytest test suites
│   ├── requirements.txt
│   └── Dockerfile
│
└── frontend/                          # Reflex App (Python-first UI)
    ├── rxconfig.py                    # Cấu hình Reflex app
    ├── requirements.txt               # Dependencies (Reflex, httpx, etc.)
    ├── studybuddy/
    │   ├── studybuddy.py              # Reflex main app & route registry
    │   ├── state/                     # Reflex State classes (Auth, Feed, Room...)
    │   ├── pages/                     # Các trang: Login, Feed, Lobby, Call, Chat...
    │   ├── components/                # Reusable game components (Navbar, Cards...)
    │   │   └── livekit_component.py   # Reflex Custom Component wrapper cho WebRTC
    │   ├── styles/                    # Design tokens & styles.css
    │   └── assets/                    # 15 chibi avatars, pixel art icons, sounds
    └── Dockerfile
```

---

## 4. Nguyên Tắc Hoạt Động Của AI Agent (Operating Protocols)

### 4.1. Quy trình làm việc: Đọc trước — Lập kế hoạch — Thực thi — Kiểm thử
1. **BẮT BUỘC ĐỌC TÀI LIỆU LIÊN QUAN TRƯỚC KHI CODE**:
   - Khi làm bất kỳ task nào, Agent **phải đọc** file `docs/tasks/task-XX-*.md` tương ứng.
   - Đối chiếu với `docs/02-database-schema.md` khi đụng đến bảng dữ liệu.
   - Đối chiếu với `docs/03-api-design.md` khi tạo hoặc gọi endpoint API.
2. **Tuân thủ thứ tự ưu tiên các tầng (Layer Priority)**:
   - **Backend**: `Model` → `Schema` → `Service` → `Router` → `Test`.
   - **Frontend**: `State` → `API Service` → `Component` → `Page` → `Style`.
3. **Kiểm tra và tự xác minh (Verification)**:
   - Backend: Viết unit/integration test với `pytest` và chạy xác nhận pass.
   - Frontend: Kiểm tra code compile sạch với `reflex run`, không có exception hay cú pháp hỏng.
4. **Quy ước Git**:
   - Branch: `feature/task-XX-ten-task` hoặc `fix/mo-ta-loi`.
   - Commit: Tuân thủ Conventional Commits (ví dụ: `feat(auth): implement JWT refresh token flow`, `fix(room): resolve race condition in join request`).

---

## 5. Quy Chuẩn Kỹ Thuật Chi Tiết (Coding Standards)

### 5.1. Backend (FastAPI & SQLAlchemy)
- **Async Everywhere**: Mọi I/O (Database, Redis, HTTP request, WebSocket) **bắt buộc** phải dùng `async` / `await`. Tuyệt đối không dùng thư viện blocking synchronous trong route handler (ví dụ: cấm dùng `requests`, phải dùng `httpx`).
- **Kiến trúc 3 lớp (3-Tier)**:
  - `routers/`: Chỉ làm nhiệm vụ nhận request, validate qua Pydantic schema, gọi service, trả HTTP status code thích hợp. Tuyệt đối không viết business logic hoặc gọi raw DB trực tiếp trong router.
  - `services/`: Chứa toàn bộ business logic, xử lý ngoại lệ nghiệp vụ, điều phối transaction DB.
  - `models/`: Định nghĩa thực thể SQLAlchemy.
- **Data Validation & Sanitization**:
  - Dùng Pydantic v2 với type annotation chặt chẽ.
  - Dùng `bleach` hoặc bộ lọc HTML để sanitize toàn bộ nội dung text nhập từ user (bài đăng, tin nhắn, bio) nhằm ngăn chặn XSS.
- **Database & Migration**:
  - Tên bảng: `snake_case` số ít (`user`, `post`, `room`, `message`...).
  - Khóa chính: Khuyến nghị dùng `UUID` (v4) để bảo mật và mở rộng.
  - Mọi thay đổi schema đều phải tạo thông qua Alembic migration (`alembic revision --autogenerate`).
- **Security & Secrets**:
  - Mật khẩu phải hash bằng `bcrypt` hoặc `argon2` qua `passlib.context.CryptContext`.
  - Không hardcode API key, Secret key, DB credential vào code. Toàn bộ đọc từ `backend/app/config.py` (sử dụng `pydantic-settings`).
- **Logging**:
  - Dùng module `logging` chuẩn của Python. Không dùng `print()` trong code production.

### 5.2. Frontend (Reflex — Python-first)
- **Triết lý Python-first**:
  - Toàn bộ giao diện, router, state management được viết bằng Python thông qua thư viện Reflex.
  - Mỗi trang là một Python module trả về component (ví dụ: `def feed_page() -> rx.Component:`).
- **Quản lý State (`rx.State`)**:
  - Tổ chức state theo module chức năng (`AuthState`, `FeedState`, `RoomState`, `ChatState`).
  - Biến state khai báo có type hints rõ ràng.
  - Event handlers phải là method của class kế thừa từ `rx.State`.
- **Styling & Design System**:
  - **KHÔNG dùng Tailwind CSS** (trừ khi có yêu cầu đặc biệt từ người dùng).
  - Sử dụng hệ thống CSS Variables định nghĩa trong `frontend/studybuddy/styles/index.css`.
  - Toàn bộ màu sắc, border radius, font chữ phải gọi qua biến hoặc class tiện ích của hệ thống game token.
- **Ngoại lệ JavaScript duy nhất (~5%)**:
  - Video Call WebRTC thông qua LiveKit Cloud: Sử dụng Reflex Custom Component (`rx.Component`) để wrap LiveKit React SDK/JS Client trong file `livekit_component.py`. Không mở rộng viết JS ở các component khác nếu không thực sự bắt buộc.

### 5.3. Design System: Phong Cách Web Game Retro
Agent phải giữ vững tính thẩm mỹ game xuyên suốt mọi màn hình:
1. **Màu sắc cốt lõi**:
   - Nền chính (Canvas): Dark Space `#0a0a1a` hoặc `#0f0f23`
   - Nền Card/Panel: `#16162e` hoặc `#1b1b3a`
   - Màu nhấn chủ đạo (Primary Accent): **Neon Green** `#00ff88`
   - Màu phụ (Secondary / Alert): **Neon Pink/Magenta** `#ff007f`, **Cyan Glow** `#00e5ff`, **Retro Gold** `#ffe600`
2. **Typography**:
   - Tiêu đề, nút bấm, nhãn chỉ số, level: Google Font **"Press Start 2P"** (pixel font).
   - Nội dung dài, đoạn văn, tin nhắn: Font **"Inter"** hoặc sans-serif sạch sẽ để đảm bảo độ đọc (readability) cho sinh viên.
3. **Hiệu ứng & Visual**:
   - Pixel art border: Viền nổi pixel (box-shadow retro dạng `2px 2px 0px #000, 4px 4px 0px var(--neon-color)`).
   - Glow effect nhẹ cho các nút hành động (Button, Online badge).
   - Micro-animations: Floating nhẹ cho avatar, pulse cho notification badge.
4. **Thuật ngữ game hóa (Gamification Language)**:
   - Bài tìm bạn học ➔ *Quest / Mission*
   - Hồ sơ người dùng ➔ *Hero Profile* (kèm EXP, Level, Star Rating)
   - Khu vực phòng học ➔ *Adventure Zones* (Math Guild, Code Dungeon, Language Tavern...)
   - 15 Avatar Chibi: Cung cấp sẵn file ảnh tại `frontend/studybuddy/assets/avatars/avatar_01.png` ... `avatar_15.png`.

---

## 6. Lộ Trình Triển Khai 12 Tasks (Roadmap)

Khi triển khai các phần việc, Agent cần bám sát thứ tự phụ thuộc sau:

| Task | Tên Task | Trọng tâm | File Hướng Dẫn |
|:---:|:---|:---|:---|
| **01** | Project Setup | Cấu hình Docker, repo, FastAPI skeleton, Reflex skeleton | `docs/tasks/task-01-project-setup.md` |
| **02** | Database Models | 10 Models SQLAlchemy, Alembic migration ban đầu, seed data mẫu | `docs/tasks/task-02-database-models.md` |
| **03** | Auth System | Register (kèm avatar), Login, JWT Auth, Token Refresh, Password Hash | `docs/tasks/task-03-auth-system.md` |
| **04** | User Profile | Xem/Sửa Profile, Upload ảnh thẻ sinh viên & CV, Đổi Avatar | `docs/tasks/task-04-user-profile.md` |
| **05** | Post Feed | CRUD bài đăng tìm bạn học offline, phân trang, lọc theo trường/môn | `docs/tasks/task-05-post-feed.md` |
| **06** | Matching Algorithm | Tính điểm tương đồng (School 40%, Location 30%, Subject 30%), Redis cache | `docs/tasks/task-06-matching-algorithm.md` |
| **07** | Room System | Tạo phòng học ảo, Lobby phân khu chủ đề, Luồng Xin vào / Duyệt qua WebSocket | `docs/tasks/task-07-room-system.md` |
| **08** | Video Call LiveKit | Tích hợp LiveKit Server SDK cấp token, Custom Component Reflex hiển thị video | `docs/tasks/task-08-video-call-livekit.md` |
| **09** | Rating System | Đánh giá 1–5 sao sau khi rời phòng, popup nhắc đánh giá, tính điểm uy tín | `docs/tasks/task-09-rating-system.md` |
| **10** | Friend & Chat | Kết bạn, danh sách bạn bè, Chat 1-1 real-time qua WebSocket + Redis Pub/Sub | `docs/tasks/task-10-friend-chat.md` |
| **11** | Frontend Game UI | Xây dựng toàn bộ giao diện Reflex: Pixel components, trang, CSS tokens, âm thanh | `docs/tasks/task-11-frontend-game-ui.md` |
| **12** | Deployment | Cấu hình Docker Production, Nginx reverse proxy, file `.env.production` | `docs/tasks/task-12-deploy.md` |

---

## 7. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

Trước khi coi một task hoặc toàn bộ dự án hoàn tất, Agent phải xác nhận đạt các tiêu chuẩn:

1. **Khởi chạy không lỗi**: `docker-compose up -d` khởi động đồng thời và ổn định 4 dịch vụ (`db`, `redis`, `backend`, `frontend`).
2. **API Specification**: Toàn bộ endpoint theo đúng `docs/03-api-design.md`, Swagger UI tại `http://localhost:8000/docs` hiển thị đầy đủ schema và response status code.
3. **Database Integrity**: Toàn bộ quan hệ Foreign Key, Index, Unique Constraint trong `docs/02-database-schema.md` được tạo đầy đủ qua Alembic migration.
4. **Trải nghiệm Game UI**: Giao diện dark mode retro game đồng nhất, có âm thanh/hiệu ứng tương tác, hoạt động mượt mà trên cả desktop và mobile view.
5. **Zero Secret Leak**: Tuyệt đối không commit file `.env`, mật khẩu hoặc secret key vào git history.

---

> *Agent Note*: Hãy luôn cập nhật trạng thái công việc vào tài liệu task khi hoàn thành từng phần và ưu tiên viết code sạch, dễ đọc, có type hint và chú thích rõ ràng.
