# API Design — StudyBuddy

Base URL: `/api/v1`

---

## 1. Authentication

### `POST /auth/register`
Đăng ký tài khoản mới.

**Request Body** (`multipart/form-data`):
```json
{
  "email": "student@example.com",
  "password": "securePass123",
  "name": "Nguyễn Văn A",
  "date_of_birth": "2002-05-15",
  "major": "Công nghệ thông tin",
  "school": "Đại học Bách Khoa HN",
  "city": "Hà Nội",
  "district": "Hai Bà Trưng",
  "address_detail": "Số 1 Đại Cồ Việt",
  "avatar_id": 3,
  "bio": "Mình thích lập trình và toán",
  "subjects": ["Giải tích 1", "Lập trình C", "IELTS"]
}
// + file: student_id_card (image, optional)
// + file: cv (pdf, optional)
```

**Response** `201`:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "Nguyễn Văn A",
    "email": "student@example.com",
    "avatar_id": 3
  }
}
```

---

### `POST /auth/login`

**Request Body**:
```json
{
  "email": "student@example.com",
  "password": "securePass123"
}
```

**Response** `200`: Same as register response.

---

### `POST /auth/refresh`

**Request Body**:
```json
{
  "refresh_token": "eyJ..."
}
```

**Response** `200`:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## 2. Users

> 🔒 Tất cả endpoint dưới đây yêu cầu `Authorization: Bearer <token>`

### `GET /users/me`
Lấy thông tin user hiện tại.

**Response** `200`:
```json
{
  "id": "uuid",
  "email": "student@example.com",
  "name": "Nguyễn Văn A",
  "date_of_birth": "2002-05-15",
  "major": "Công nghệ thông tin",
  "school": "Đại học Bách Khoa HN",
  "city": "Hà Nội",
  "district": "Hai Bà Trưng",
  "avatar_id": 3,
  "bio": "Mình thích lập trình và toán",
  "avg_rating": 4.5,
  "total_ratings": 12,
  "subjects": ["Giải tích 1", "Lập trình C", "IELTS"],
  "created_at": "2026-01-15T10:30:00Z"
}
```

### `PUT /users/me`
Cập nhật profile. Chỉ gửi các field muốn thay đổi.

### `GET /users/{user_id}`
Xem profile người khác (public info only).

---

## 3. Posts (Bảng tin)

### `POST /posts`
Tạo bài đăng mới.

**Request Body**:
```json
{
  "content": "Tìm bạn học Giải tích 1 cuối tuần này, khu vực Cầu Giấy",
  "study_type": "offline",
  "location": "Quán cafe ABC, Cầu Giấy",
  "preferred_school": "",
  "study_date": "2026-09-28T14:00:00Z",
  "max_people": 4,
  "tags": ["giai-tich", "toan"]
}
```

**Response** `201`:
```json
{
  "id": "uuid",
  "content": "...",
  "study_type": "offline",
  "author": {
    "id": "uuid",
    "name": "Nguyễn Văn A",
    "avatar_id": 3,
    "school": "ĐHBK HN",
    "avg_rating": 4.5
  },
  "tags": ["giai-tich", "toan"],
  "created_at": "2026-09-23T10:00:00Z"
}
```

---

### `GET /posts/feed`
Lấy bảng tin đã qua matching algorithm.

**Query params**:
| Param | Type | Default | Mô tả |
|-------|------|---------|--------|
| `page` | int | 1 | Trang |
| `per_page` | int | 20 | Số bài/trang (max 50) |
| `study_type` | string | | Filter: "online" / "offline" |
| `tag` | string | | Filter theo tag |

**Response** `200`:
```json
{
  "items": [
    {
      "id": "uuid",
      "content": "...",
      "study_type": "offline",
      "relevance_score": 8.5,
      "author": { "id": "...", "name": "...", "avatar_id": 5, "school": "...", "avg_rating": 4.2 },
      "tags": ["giai-tich"],
      "created_at": "2026-09-23T10:00:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8
}
```

### `GET /posts/{post_id}` — Chi tiết bài đăng
### `PUT /posts/{post_id}` — Sửa bài (chỉ author)
### `DELETE /posts/{post_id}` — Xóa bài (soft delete, chỉ author)

---

## 4. Rooms (Phòng học)

### `POST /rooms`
Tạo phòng học mới.

**Request Body**:
```json
{
  "name": "Ôn thi Giải tích nhóm",
  "topic": "Giải tích 1 - Chương 3: Tích phân",
  "category_id": "uuid-of-toan-hoc",
  "max_participants": 6
}
```

**Response** `201`:
```json
{
  "id": "uuid",
  "name": "Ôn thi Giải tích nhóm",
  "room_code": "ABC123",
  "topic": "...",
  "category": { "id": "...", "name": "Toán học", "icon": "📐", "color": "#FF6B6B" },
  "host": { "id": "...", "name": "...", "avatar_id": 3 },
  "status": "waiting",
  "max_participants": 6,
  "current_participants": 1,
  "created_at": "..."
}
```

---

### `GET /rooms`
Danh sách phòng đang hoạt động (lobby).

**Query params**:
| Param | Type | Default | Mô tả |
|-------|------|---------|--------|
| `page` | int | 1 | |
| `per_page` | int | 20 | |
| `category_id` | uuid | | Filter theo khu vực |
| `status` | string | "waiting,active" | |
| `search` | string | | Tìm theo tên/topic |

---

### `GET /rooms/categories`
Danh sách các khu vực (category) + số phòng đang active.

**Response** `200`:
```json
[
  {
    "id": "uuid",
    "name": "Toán học",
    "icon": "📐",
    "color": "#FF6B6B",
    "active_rooms_count": 5
  }
]
```

---

### `GET /rooms/{room_id}`
Chi tiết phòng + danh sách participants.

### `POST /rooms/{room_id}/request`
Gửi request xin vào phòng.

**Response** `201`:
```json
{
  "participant_id": "uuid",
  "status": "pending",
  "message": "Yêu cầu đã được gửi tới host"
}
```

> ⚡ Side-effect: Gửi WebSocket event tới host

---

### `POST /rooms/{room_id}/approve/{user_id}`
Host chấp nhận request. Chỉ host mới có quyền.

**Response** `200`:
```json
{
  "status": "accepted",
  "livekit_token": "eyJ...",
  "livekit_url": "wss://your-app.livekit.cloud"
}
```

> ⚡ Side-effect: Gửi WebSocket event + LiveKit token tới user được approve

---

### `POST /rooms/{room_id}/reject/{user_id}`
Host từ chối request.

### `POST /rooms/{room_id}/leave`
User rời phòng. Trigger rating popup ở frontend.

### `POST /rooms/{room_id}/close`
Host đóng phòng. Kick tất cả participants.

### `GET /rooms/{room_id}/token`
Lấy LiveKit token (chỉ cho participant đã được approve).

---

## 5. Ratings (Đánh giá)

### `POST /ratings`

**Request Body**:
```json
{
  "ratee_id": "uuid",
  "room_id": "uuid",
  "stars": 4,
  "comment": "Bạn giải thích rất dễ hiểu!"
}
```

**Validation**:
- Rater phải từng ở cùng phòng với ratee
- Không tự rate chính mình
- Mỗi cặp (rater, ratee, room) chỉ rate 1 lần

**Response** `201`:
```json
{
  "id": "uuid",
  "stars": 4,
  "comment": "...",
  "created_at": "..."
}
```

> ⚡ Side-effect: Cập nhật `user.avg_rating` và `user.total_ratings`

---

### `GET /users/{user_id}/ratings`
Xem danh sách đánh giá của 1 user.

**Query params**: `page`, `per_page`

---

## 6. Friends (Kết bạn)

### `POST /friends/request/{user_id}`
Gửi lời mời kết bạn.

### `POST /friends/accept/{friendship_id}`
Chấp nhận lời mời.

### `POST /friends/reject/{friendship_id}`
Từ chối lời mời.

### `DELETE /friends/{user_id}`
Hủy kết bạn.

### `GET /friends`
Danh sách bạn bè.

**Response** `200`:
```json
{
  "items": [
    {
      "friendship_id": "uuid",
      "friend": {
        "id": "uuid",
        "name": "Trần Thị B",
        "avatar_id": 7,
        "school": "ĐHQG HN",
        "is_online": true
      },
      "since": "2026-08-01T00:00:00Z"
    }
  ]
}
```

### `GET /friends/requests`
Danh sách lời mời kết bạn đang chờ (incoming).

---

## 7. Messages (Nhắn tin)

### `GET /messages/conversations`
Danh sách conversations (friend list có tin nhắn gần nhất).

**Response** `200`:
```json
{
  "items": [
    {
      "friend": { "id": "...", "name": "...", "avatar_id": 7, "is_online": true },
      "last_message": {
        "content": "OK mai gặp nhé!",
        "created_at": "2026-09-23T15:30:00Z",
        "is_mine": false
      },
      "unread_count": 2
    }
  ]
}
```

### `GET /messages/{friend_id}`
Lịch sử tin nhắn với 1 friend.

**Query params**: `page`, `per_page`, `before` (cursor-based pagination)

### `POST /messages/{friend_id}/read`
Đánh dấu tất cả tin nhắn từ friend này là đã đọc.

> 💡 Gửi tin nhắn mới thực hiện qua **WebSocket**, không qua REST API.

---

## 8. WebSocket Endpoints

### `WS /ws/notifications`
Kết nối khi user login. Nhận các event:

```typescript
// Event types
type WSEvent =
  | { type: "room_request"; data: { room_id: string; user: UserBrief } }
  | { type: "room_approved"; data: { room_id: string; livekit_token: string } }
  | { type: "room_rejected"; data: { room_id: string } }
  | { type: "friend_request"; data: { friendship_id: string; from: UserBrief } }
  | { type: "friend_accepted"; data: { friendship_id: string; friend: UserBrief } }
  | { type: "new_message"; data: { from: string; content: string; created_at: string } }
  | { type: "user_online"; data: { user_id: string } }
  | { type: "user_offline"; data: { user_id: string } }
```

**Auth**: Gửi token trong query param: `/ws/notifications?token=<jwt>`

---

### `WS /ws/chat/{friend_id}`
Chat real-time với 1 friend cụ thể.

**Send**:
```json
{ "type": "message", "content": "Xin chào!" }
{ "type": "typing" }
{ "type": "stop_typing" }
```

**Receive**:
```json
{ "type": "message", "content": "...", "created_at": "...", "message_id": "uuid" }
{ "type": "typing" }
{ "type": "stop_typing" }
{ "type": "read", "read_at": "..." }
```

---

## 9. File Upload

### `POST /upload/student-id`
Upload ảnh thẻ sinh viên.

**Request**: `multipart/form-data`, field `file` (image, max 5MB)
**Response**: `{ "url": "/uploads/student-ids/uuid.jpg" }`

### `POST /upload/cv`
Upload file CV.

**Request**: `multipart/form-data`, field `file` (pdf, max 10MB)
**Response**: `{ "url": "/uploads/cvs/uuid.pdf" }`

---

## 10. Error Response Format

Tất cả error trả về dạng thống nhất:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email đã tồn tại",
    "details": [
      { "field": "email", "message": "Email này đã được đăng ký" }
    ]
  }
}
```

**Error codes**:
| HTTP | Code | Mô tả |
|------|------|--------|
| 400 | `VALIDATION_ERROR` | Dữ liệu input không hợp lệ |
| 401 | `UNAUTHORIZED` | Chưa đăng nhập / token hết hạn |
| 403 | `FORBIDDEN` | Không có quyền thực hiện |
| 404 | `NOT_FOUND` | Resource không tồn tại |
| 409 | `CONFLICT` | Conflict (ví dụ: đã gửi request rồi) |
| 429 | `RATE_LIMITED` | Quá nhiều request |
| 500 | `INTERNAL_ERROR` | Lỗi server |
