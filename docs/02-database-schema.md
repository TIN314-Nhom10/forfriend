# Database Schema — StudyBuddy

## 1. Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ ROOM : hosts
    USER ||--o{ ROOM_PARTICIPANT : joins
    USER ||--o{ RATING : "gives/receives"
    USER ||--o{ FRIENDSHIP : has
    USER ||--o{ MESSAGE : sends

    ROOM ||--o{ ROOM_PARTICIPANT : contains
    ROOM ||--o{ RATING : generates
    ROOM }o--|| ROOM_CATEGORY : belongs_to

    POST }o--o{ POST_TAG : has
    USER }o--o{ USER_SUBJECT : studies

    USER {
        uuid id PK
        string email UK
        string password_hash
        string name
        date date_of_birth
        string major
        string school
        string city
        string district
        string address_detail
        string student_id_card_url
        string cv_url
        int avatar_id
        string bio
        float avg_rating
        int total_ratings
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    POST {
        uuid id PK
        uuid author_id FK
        string content
        string study_type "online|offline"
        string location
        string preferred_school
        timestamp study_date
        int max_people
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    POST_TAG {
        uuid id PK
        uuid post_id FK
        string tag_name
    }

    USER_SUBJECT {
        uuid id PK
        uuid user_id FK
        string subject_name
    }

    ROOM {
        uuid id PK
        uuid host_id FK
        string name
        string topic
        uuid category_id FK
        string room_code UK
        string status "waiting|active|closed"
        int max_participants
        int current_participants
        timestamp created_at
        timestamp closed_at
    }

    ROOM_CATEGORY {
        uuid id PK
        string name UK
        string icon
        string color
        int display_order
    }

    ROOM_PARTICIPANT {
        uuid id PK
        uuid room_id FK
        uuid user_id FK
        string status "pending|accepted|rejected|left"
        timestamp requested_at
        timestamp joined_at
        timestamp left_at
    }

    RATING {
        uuid id PK
        uuid rater_id FK
        uuid ratee_id FK
        uuid room_id FK
        int stars "1-5"
        string comment
        timestamp created_at
    }

    FRIENDSHIP {
        uuid id PK
        uuid requester_id FK
        uuid addressee_id FK
        string status "pending|accepted|rejected|blocked"
        timestamp created_at
        timestamp responded_at
    }

    MESSAGE {
        uuid id PK
        uuid sender_id FK
        uuid receiver_id FK
        string content
        boolean is_read
        timestamp created_at
        timestamp read_at
    }
```

---

## 2. Chi tiết từng bảng

### 2.1. `user`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK, default uuid4 | |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Email đăng nhập |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hash |
| `name` | VARCHAR(100) | NOT NULL | Tên hiển thị |
| `date_of_birth` | DATE | NOT NULL | Năm sinh |
| `major` | VARCHAR(100) | NOT NULL | Ngành học |
| `school` | VARCHAR(200) | NOT NULL | Trường |
| `city` | VARCHAR(100) | NOT NULL | Thành phố |
| `district` | VARCHAR(100) | | Quận/Huyện |
| `address_detail` | TEXT | | Địa chỉ chi tiết |
| `student_id_card_url` | VARCHAR(500) | | URL ảnh thẻ sinh viên |
| `cv_url` | VARCHAR(500) | | URL file CV |
| `avatar_id` | INTEGER | NOT NULL, default 1 | ID avatar chibi (1–15) |
| `bio` | TEXT | | Giới thiệu bản thân |
| `avg_rating` | FLOAT | default 0.0 | Rating trung bình (denormalized) |
| `total_ratings` | INTEGER | default 0 | Tổng lượt đánh giá |
| `is_active` | BOOLEAN | default true | Tài khoản còn active? |
| `created_at` | TIMESTAMP | default now() | |
| `updated_at` | TIMESTAMP | on update | |

**Indexes:**
- `idx_user_school` on (`school`)
- `idx_user_city` on (`city`)
- `idx_user_major` on (`major`)

---

### 2.2. `user_subject`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `user_id` | UUID | FK → user.id, NOT NULL | |
| `subject_name` | VARCHAR(100) | NOT NULL | Tên môn học (ví dụ: "Giải tích 1") |

**Indexes:**
- `idx_user_subject_user` on (`user_id`)
- UNIQUE constraint on (`user_id`, `subject_name`)

---

### 2.3. `post`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `author_id` | UUID | FK → user.id, NOT NULL | |
| `content` | TEXT | NOT NULL | Nội dung bài đăng |
| `study_type` | VARCHAR(10) | NOT NULL, "online" or "offline" | Loại học |
| `location` | VARCHAR(200) | | Địa điểm (cho offline) |
| `preferred_school` | VARCHAR(200) | | Ưu tiên trường nào |
| `study_date` | TIMESTAMP | | Thời gian muốn học |
| `max_people` | INTEGER | default 5 | Tối đa bao nhiêu người |
| `is_active` | BOOLEAN | default true | Bài còn hiệu lực? |
| `created_at` | TIMESTAMP | default now() | |
| `updated_at` | TIMESTAMP | on update | |

**Indexes:**
- `idx_post_author` on (`author_id`)
- `idx_post_created` on (`created_at` DESC)
- `idx_post_active` on (`is_active`, `created_at` DESC)

---

### 2.4. `post_tag`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `post_id` | UUID | FK → post.id, NOT NULL, ON DELETE CASCADE | |
| `tag_name` | VARCHAR(50) | NOT NULL | Tag: "toan", "lap-trinh", "ielts"... |

**Indexes:**
- `idx_post_tag_post` on (`post_id`)
- `idx_post_tag_name` on (`tag_name`)

---

### 2.5. `room`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `host_id` | UUID | FK → user.id, NOT NULL | Người tạo phòng |
| `name` | VARCHAR(100) | NOT NULL | Tên phòng |
| `topic` | VARCHAR(200) | NOT NULL | Chủ đề phòng |
| `category_id` | UUID | FK → room_category.id | Khu vực phân loại |
| `room_code` | VARCHAR(10) | UNIQUE, NOT NULL | Mã phòng ngắn |
| `status` | VARCHAR(20) | NOT NULL, default "waiting" | waiting → active → closed |
| `max_participants` | INTEGER | NOT NULL, default 10 | Giới hạn người |
| `current_participants` | INTEGER | default 1 | Số người hiện tại (denormalized) |
| `created_at` | TIMESTAMP | default now() | |
| `closed_at` | TIMESTAMP | | Khi phòng đóng |

**Indexes:**
- `idx_room_host` on (`host_id`)
- `idx_room_category` on (`category_id`)
- `idx_room_status` on (`status`, `created_at` DESC)
- `idx_room_code` on (`room_code`)

---

### 2.6. `room_category`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL | "Toán học", "Lập trình", "Ngoại ngữ"... |
| `icon` | VARCHAR(10) | | Emoji hoặc icon code |
| `color` | VARCHAR(7) | | Hex color cho UI |
| `display_order` | INTEGER | default 0 | Thứ tự hiển thị |

**Seed data:**

| name | icon | color |
|------|------|-------|
| Toán học | 📐 | #FF6B6B |
| Lập trình | 💻 | #4ECDC4 |
| Ngoại ngữ | 🌍 | #45B7D1 |
| Khoa học tự nhiên | 🔬 | #96CEB4 |
| Kinh tế | 📊 | #FECA57 |
| Y - Dược | ⚕️ | #FF9FF3 |
| Luật | ⚖️ | #54A0FF |
| Kỹ thuật | ⚙️ | #5F27CD |
| Nghệ thuật | 🎨 | #FF6348 |
| Khác | 📚 | #A0A0A0 |

---

### 2.7. `room_participant`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `room_id` | UUID | FK → room.id, NOT NULL | |
| `user_id` | UUID | FK → user.id, NOT NULL | |
| `status` | VARCHAR(20) | NOT NULL, default "pending" | pending → accepted/rejected/left |
| `requested_at` | TIMESTAMP | default now() | |
| `joined_at` | TIMESTAMP | | Khi được accept |
| `left_at` | TIMESTAMP | | Khi rời phòng |

**Indexes:**
- `idx_rp_room` on (`room_id`, `status`)
- `idx_rp_user` on (`user_id`)
- UNIQUE constraint on (`room_id`, `user_id`)

---

### 2.8. `rating`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `rater_id` | UUID | FK → user.id, NOT NULL | Người đánh giá |
| `ratee_id` | UUID | FK → user.id, NOT NULL | Người bị đánh giá |
| `room_id` | UUID | FK → room.id, NOT NULL | Phòng liên quan |
| `stars` | INTEGER | NOT NULL, CHECK (1–5) | Số sao |
| `comment` | TEXT | | Nhận xét (tùy chọn) |
| `created_at` | TIMESTAMP | default now() | |

**Indexes:**
- `idx_rating_ratee` on (`ratee_id`)
- UNIQUE constraint on (`rater_id`, `ratee_id`, `room_id`) — 1 lần rate/người/phòng

---

### 2.9. `friendship`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `requester_id` | UUID | FK → user.id, NOT NULL | Người gửi lời mời |
| `addressee_id` | UUID | FK → user.id, NOT NULL | Người nhận |
| `status` | VARCHAR(20) | NOT NULL, default "pending" | pending → accepted/rejected/blocked |
| `created_at` | TIMESTAMP | default now() | |
| `responded_at` | TIMESTAMP | | Khi phản hồi |

**Indexes:**
- `idx_friend_requester` on (`requester_id`, `status`)
- `idx_friend_addressee` on (`addressee_id`, `status`)
- UNIQUE constraint on (`requester_id`, `addressee_id`)
- CHECK constraint: `requester_id != addressee_id`

---

### 2.10. `message`

| Column | Type | Constraints | Mô tả |
|--------|------|------------|--------|
| `id` | UUID | PK | |
| `sender_id` | UUID | FK → user.id, NOT NULL | |
| `receiver_id` | UUID | FK → user.id, NOT NULL | |
| `content` | TEXT | NOT NULL | Nội dung tin nhắn |
| `is_read` | BOOLEAN | default false | Đã đọc chưa |
| `created_at` | TIMESTAMP | default now() | |
| `read_at` | TIMESTAMP | | Thời điểm đọc |

**Indexes:**
- `idx_msg_conversation` on (`sender_id`, `receiver_id`, `created_at` DESC)
- `idx_msg_unread` on (`receiver_id`, `is_read`) WHERE is_read = false

---

## 3. Migration Strategy

Sử dụng **Alembic** để quản lý migration:

```bash
# Khởi tạo
alembic init alembic

# Tạo migration mới
alembic revision --autogenerate -m "create_initial_tables"

# Chạy migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

Thứ tự migration:
1. `room_category` (seed data)
2. `user`
3. `user_subject`
4. `post` + `post_tag`
5. `room` + `room_participant`
6. `rating`
7. `friendship`
8. `message`
