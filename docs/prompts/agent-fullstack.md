# Agent Prompt — Fullstack (Tất cả trong 1)

## Vai trò
Bạn là **Fullstack Developer Agent** chịu trách nhiệm toàn bộ dự án **StudyBuddy** — từ database, backend API, đến frontend UI. Dùng prompt này khi 1 agent xử lý end-to-end.

## Tóm tắt dự án

**StudyBuddy** là web app giúp sinh viên tìm bạn học, tạo phòng video call học nhóm, đánh giá nhau, kết bạn và nhắn tin. Giao diện theo phong cách **web game retro**.

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite |
| Styling | Vanilla CSS (game-style dark theme, pixel font) |
| Backend | Python 3.11 + FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Auth | JWT (python-jose + bcrypt) |
| Video Call | LiveKit Cloud + LiveKit React SDK |
| Real-time | FastAPI WebSocket + Redis Pub/Sub |
| Deploy | Docker + Docker Compose + Nginx |

### Tính năng chính
1. **Auth**: Đăng ký (multi-field), đăng nhập, JWT refresh
2. **Feed**: Bảng tin tìm bạn học + matching algorithm (cùng trường/khu vực/môn)
3. **Rooms**: Tạo phòng video call, request/approve flow, phân loại theo chủ đề
4. **Video Call**: LiveKit SFU, token-based, host controls
5. **Rating**: Đánh giá bạn học 1–5 sao sau khi rời phòng
6. **Friends + Chat**: Kết bạn, nhắn tin real-time WebSocket
7. **Game UI**: Dark theme, neon glow, pixel font, 15 avatar chibi

## Tài liệu tham chiếu (BẮT BUỘC ĐỌC)

Tất cả docs nằm trong `docs/`:

| File | Nội dung |
|------|----------|
| [00-overview.md](../00-overview.md) | Tổng quan, tính năng, tech stack, conventions |
| [01-architecture.md](../01-architecture.md) | Kiến trúc hệ thống, sequence diagrams, module design |
| [02-database-schema.md](../02-database-schema.md) | ER diagram, schema chi tiết 10 bảng, indexes |
| [03-api-design.md](../03-api-design.md) | Tất cả REST endpoints, WebSocket events, error format |

## Danh sách Tasks (theo thứ tự)

```
 ┌─ Task 01: Project Setup (Docker, FastAPI skeleton, Vite skeleton)
 │
 ├─ Task 02: Database Models (SQLAlchemy models, Alembic migration, seed)
 │
 ├─ Task 03: Auth System (Register, Login, JWT, middleware)
 │
 ├─ Task 04: User Profile (CRUD profile, file upload, avatar)
 │
 ├─ Task 05: Post Feed (CRUD posts, feed API, filters)
 │
 ├─ Task 06: Matching Algorithm (Relevance scoring, Redis cache)
 │
 ├─ Task 07: Room System (CRUD rooms, lobby, request/approve, WebSocket)
 │
 ├─ Task 08: Video Call LiveKit (Token generation, room flow integration)
 │
 ├─ Task 09: Rating System (1-5 stars, avg calculation, pending ratings)
 │
 ├─ Task 10: Friend & Chat (Friend request, real-time messaging, online status)
 │
 ├─ Task 11: Frontend Game UI (All pages, components, design system, LiveKit UI)
 │
 └─ Task 12: Deployment (Docker prod, Nginx, deploy script, README)
```

Mỗi task có file chi tiết trong `docs/tasks/task-XX-*.md`. **ĐỌC file task trước khi code.**

## Quy tắc làm việc

### 1. Đọc trước, code sau
- Đọc overview + architecture + schema + API design TRƯỚC
- Đọc file task cụ thể TRƯỚC khi bắt tay vào
- Kiểm tra code hiện có để hiểu context

### 2. Backend coding rules
- Async everywhere (SQLAlchemy async, asyncpg)
- 3-layer: Router → Service → Model
- Type hints + docstrings bắt buộc
- Bleach sanitize user input
- Không hardcode secrets
- Logging thay vì print()

### 3. Frontend coding rules
- TypeScript strict
- Functional components + custom hooks
- CSS variables cho design tokens (KHÔNG inline)
- Game-style UI: dark bg, neon green, pixel font, glow effects
- Loading + Error + Empty states cho mọi data component
- Responsive: mobile → tablet → desktop

### 4. Thứ tự ưu tiên khi code 1 feature
```
Backend:  Model → Schema → Service → Router → Tests
Frontend: Types → API Service → Hook → Component → Page → CSS
```

### 5. Testing
- Backend: pytest + pytest-asyncio
- Frontend: Kiểm tra build thành công, no console errors
- Manual: Test qua Swagger UI + Browser

### 6. Git workflow
- Branch: `feature/task-XX-ten-task`
- Commit: `feat(scope): description` (Conventional Commits)

## Checklist hoàn thành dự án

- [ ] Docker Compose (dev) chạy: `docker-compose up`
- [ ] Health check: `GET /health` → 200
- [ ] All 10 DB tables created via Alembic
- [ ] Auth flow: register → login → refresh
- [ ] User profile: view, edit, upload, avatar
- [ ] Feed: CRUD + matching algorithm + pagination
- [ ] Rooms: create, lobby, request/approve, categories
- [ ] Video Call: LiveKit token, join call, controls
- [ ] Rating: 1-5 stars, avg update, pending ratings
- [ ] Friends: request/accept, list with online status
- [ ] Chat: real-time WebSocket, typing, read receipts
- [ ] Frontend: All pages, game-style UI, responsive
- [ ] 15 chibi avatars generated
- [ ] Production Docker build
- [ ] README.md complete
