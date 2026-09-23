# Kiến Trúc Hệ Thống — StudyBuddy

## 1. Kiến trúc tổng quan (High-Level Architecture)

```mermaid
graph TB
    subgraph Client["🐍 Frontend (Reflex — Python-first)"]
        UI["Game-style UI (Python)"]
        WS_Client["Reflex State / WebSocket"]
        LK_Client["LiveKit JS Component (ngoại lệ)"]
    end

    subgraph API["🐍 Backend (FastAPI)"]
        REST["REST API Routes"]
        WS_Server["WebSocket Handler"]
        AUTH["Auth Middleware (JWT)"]
        MATCH["Matching Engine"]
        BIZ["Business Services"]
    end

    subgraph Data["💾 Data Layer"]
        PG["PostgreSQL"]
        REDIS["Redis (Cache + Pub/Sub)"]
    end

    subgraph Media["📹 Media Layer"]
        LK_SFU["LiveKit SFU Server (Cloud)"]
    end

    UI -->|HTTP/REST| REST
    WS_Client -->|WebSocket| WS_Server
    LK_Client <-->|WebRTC| LK_SFU

    REST --> AUTH
    AUTH --> BIZ
    BIZ --> MATCH
    BIZ --> PG
    BIZ --> REDIS
    WS_Server --> REDIS
    REST -->|Generate Token| LK_SFU
```

---

## 2. Luồng dữ liệu chính (Data Flow)

### 2.1. Đăng ký & Đăng nhập

```mermaid
sequenceDiagram
    actor U as User
    participant FE as Frontend
    participant BE as FastAPI
    participant DB as PostgreSQL

    U->>FE: Điền form đăng ký + chọn avatar
    FE->>BE: POST /api/v1/auth/register
    BE->>BE: Hash password (bcrypt)
    BE->>DB: INSERT user
    DB-->>BE: user_id
    BE-->>FE: { access_token, refresh_token }
    FE->>FE: Lưu token vào localStorage
    FE-->>U: Redirect → Dashboard
```

### 2.2. Bảng tin & Matching Algorithm

```mermaid
sequenceDiagram
    actor U as User
    participant FE as Frontend
    participant BE as FastAPI
    participant DB as PostgreSQL
    participant RD as Redis

    U->>FE: Mở bảng tin (Feed)
    FE->>BE: GET /api/v1/posts/feed?page=1
    BE->>DB: Query posts
    BE->>BE: Matching Score = f(school, area, subject)
    Note over BE: Score = w1*(same_school) + w2*(same_area) + w3*(same_subject)
    BE->>RD: Cache kết quả feed (TTL 5 phút)
    BE-->>FE: [posts sorted by relevance_score DESC]
    FE-->>U: Hiển thị bảng tin

    U->>FE: Tạo bài đăng mới
    FE->>BE: POST /api/v1/posts
    BE->>DB: INSERT post
    BE->>RD: Invalidate feed cache liên quan
    BE-->>FE: { post_id, created_at }
```

### 2.3. Tạo phòng & Video Call

```mermaid
sequenceDiagram
    actor Host as Host
    actor Guest as Guest
    participant FE as Frontend
    participant BE as FastAPI
    participant DB as PostgreSQL
    participant LK as LiveKit Cloud

    Host->>FE: Tạo phòng (tên, chủ đề, max người)
    FE->>BE: POST /api/v1/rooms
    BE->>DB: INSERT room (status=active)
    BE-->>FE: { room_id, room_code }

    Guest->>FE: Xem danh sách phòng → Bấm "Xin vào"
    FE->>BE: POST /api/v1/rooms/{id}/request
    BE->>DB: INSERT room_participant (status=pending)
    BE-->>Host: WebSocket event: "new_request"

    Host->>FE: Bấm "Chấp nhận"
    FE->>BE: POST /api/v1/rooms/{id}/approve/{user_id}
    BE->>DB: UPDATE room_participant (status=accepted)
    BE->>LK: Generate access token (room, identity)
    LK-->>BE: JWT token
    BE-->>Guest: WebSocket event: "approved" + livekit_token

    Guest->>FE: Nhận token → Connect LiveKit
    FE->>LK: Join room (WebRTC)
    LK-->>FE: Media streams (audio + video)
```

### 2.4. Nhắn tin riêng (Real-time Chat)

```mermaid
sequenceDiagram
    actor A as User A
    actor B as User B
    participant FE_A as Frontend A
    participant FE_B as Frontend B
    participant BE as FastAPI (WebSocket)
    participant DB as PostgreSQL
    participant RD as Redis Pub/Sub

    A->>FE_A: Gõ tin nhắn → Gửi
    FE_A->>BE: WS message: {to: B, content: "Hello!"}
    BE->>DB: INSERT message
    BE->>RD: PUBLISH channel:user:B
    RD-->>BE: Subscriber for user B
    BE-->>FE_B: WS message: {from: A, content: "Hello!"}
    FE_B-->>B: Hiển thị tin nhắn + notification sound
```

---

## 3. Thiết kế module Backend

```mermaid
graph LR
    subgraph Routers["📡 Routers (API Layer)"]
        R_AUTH["auth.py"]
        R_USER["users.py"]
        R_POST["posts.py"]
        R_ROOM["rooms.py"]
        R_RATE["ratings.py"]
        R_FRIEND["friends.py"]
        R_MSG["messages.py"]
    end

    subgraph Services["⚙️ Services (Business Logic)"]
        S_AUTH["AuthService"]
        S_USER["UserService"]
        S_POST["PostService"]
        S_ROOM["RoomService"]
        S_RATE["RatingService"]
        S_FRIEND["FriendService"]
        S_MSG["MessageService"]
        S_MATCH["MatchingService"]
        S_LK["LiveKitService"]
    end

    subgraph Models["🗄️ Models (Data Layer)"]
        M_USER["User"]
        M_POST["Post"]
        M_ROOM["Room"]
        M_PART["RoomParticipant"]
        M_RATE["Rating"]
        M_FRIEND["Friendship"]
        M_MSG["Message"]
    end

    R_AUTH --> S_AUTH
    R_USER --> S_USER
    R_POST --> S_POST
    R_POST --> S_MATCH
    R_ROOM --> S_ROOM
    R_ROOM --> S_LK
    R_RATE --> S_RATE
    R_FRIEND --> S_FRIEND
    R_MSG --> S_MSG

    S_AUTH --> M_USER
    S_USER --> M_USER
    S_POST --> M_POST
    S_ROOM --> M_ROOM
    S_ROOM --> M_PART
    S_RATE --> M_RATE
    S_FRIEND --> M_FRIEND
    S_MSG --> M_MSG
    S_MATCH --> M_USER
    S_MATCH --> M_POST
```

---

## 4. Thiết kế module Frontend

```mermaid
graph TB
    subgraph Pages["📄 Pages (Python)"]
        P_LOGIN["login.py"]
        P_REG["register.py"]
        P_DASH["dashboard.py"]
        P_FEED["feed.py"]
        P_ROOMS["room_lobby.py"]
        P_CALL["video_call.py"]
        P_CHAT["chat.py"]
        P_PROFILE["profile.py"]
    end

    subgraph Components["🧩 Components (Python)"]
        C_NAV["game_navbar.py"]
        C_POST["post_card.py"]
        C_ROOM["room_card.py"]
        C_AVATAR["avatar_selector.py"]
        C_RATING["star_rating.py"]
        C_MSG["message_bubble.py"]
        C_NOTIF["notification_toast.py"]
        C_VIDEO["livekit_component.py ⚠️JS"]
    end

    subgraph State["🗄️ Reflex State (Python)"]
        S_AUTH["AuthState"]
        S_FEED["FeedState"]
        S_ROOM["RoomState"]
        S_CHAT["ChatState"]
        S_NOTIF["NotificationState"]
    end

    subgraph Services_FE["📡 API Services (Python)"]
        API["httpx async client"]
        WS["Reflex WebSocket / EventHandler"]
    end

    P_FEED --> C_POST
    P_ROOMS --> C_ROOM
    P_CALL --> C_VIDEO
    P_CHAT --> C_MSG
    P_REG --> C_AVATAR

    Pages --> State
    State --> Services_FE
```

---

## 5. Chiến lược Matching Algorithm

Thuật toán đẩy bài đăng/phòng phù hợp tới user dựa trên **điểm tương đồng (Relevance Score)**:

```
relevance_score(user, post) = 
    w1 * same_school(user, post.author)      // 0 hoặc 1, weight = 3.0
  + w2 * same_area(user, post.author)        // 0 hoặc 1, weight = 2.0  
  + w3 * subject_overlap(user, post)         // 0.0 → 1.0, weight = 2.5
  + w4 * recency_decay(post.created_at)      // 0.0 → 1.0, weight = 1.0
  + w5 * author_rating(post.author)          // 0.0 → 1.0, weight = 1.5
```

| Factor | Giải thích | Weight |
|--------|-----------|--------|
| `same_school` | Cùng trường → 1, khác → 0 | 3.0 |
| `same_area` | Cùng khu vực (quận/thành phố) → 1 | 2.0 |
| `subject_overlap` | % môn học chung (dựa trên tags) | 2.5 |
| `recency_decay` | Bài mới hơn được ưu tiên, decay theo giờ | 1.0 |
| `author_rating` | Rating trung bình của author / 5 | 1.5 |

Sắp xếp kết quả theo `relevance_score DESC`, phân trang 20 bài/trang.

---

## 6. Bảo mật (Security)

- **Authentication**: JWT Access Token (15 phút) + Refresh Token (7 ngày)
- **Password**: Hash bằng bcrypt, salt rounds = 12
- **API Protection**: Tất cả endpoint (trừ auth) yêu cầu Bearer token
- **WebSocket Auth**: Gửi token trong message đầu tiên khi connect
- **LiveKit Token**: Server-side generation, TTL = thời gian session
- **CORS**: Chỉ allow origin từ frontend domain
- **Rate Limiting**: slowapi, 60 req/phút cho API thường, 5 req/phút cho auth
- **Input Validation**: Pydantic v2 validate mọi input, bleach sanitize text content
- **File Upload**: Validate file type + size (max 5MB cho student ID, 10MB cho CV)

---

## 7. Scalability Notes

Ở giai đoạn MVP, hệ thống chạy trên **single server** (Docker Compose) là đủ. Khi scale:

1. **Database**: Thêm read replica cho PostgreSQL
2. **WebSocket**: Chuyển sang Redis Pub/Sub để scale horizontal
3. **Video Call**: LiveKit Cloud tự scale, không cần lo
4. **Cache**: Redis cluster
5. **Backend**: Chạy nhiều FastAPI instances sau Nginx load balancer
