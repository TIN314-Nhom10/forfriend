# Task 02 — Database Models & Migrations

## Mục tiêu
Tạo tất cả SQLAlchemy models theo schema đã thiết kế trong `docs/02-database-schema.md`, cấu hình Alembic migration, và seed data cho `room_category`.

## Phụ thuộc
- Task 01 (Project Setup) — cần `database.py`, `Base`, alembic config

## Tham chiếu
- [02-database-schema.md](../02-database-schema.md) — Schema chi tiết cho từng bảng

## Yêu cầu chi tiết

### 2.1. SQLAlchemy Models

Tạo các file trong `backend/app/models/`:

```
models/
├── __init__.py          # Import tất cả models, export Base
├── user.py              # User, UserSubject
├── post.py              # Post, PostTag
├── room.py              # Room, RoomCategory, RoomParticipant
├── rating.py            # Rating
├── friendship.py        # Friendship
└── message.py           # Message
```

**Quy ước chung cho mọi model:**
- Dùng `mapped_column` syntax mới của SQLAlchemy 2.0
- UUID primary key dùng `uuid.uuid4` default
- Timestamps dùng `func.now()` server default
- Relationship khai báo với `back_populates`
- Type hints bắt buộc cho tất cả columns
- Docstring cho class

**Ví dụ mẫu cho `user.py`:**
```python
import uuid
from datetime import date, datetime
from sqlalchemy import String, Integer, Float, Boolean, Date, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    """Bảng user — thông tin sinh viên."""
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    major: Mapped[str] = mapped_column(String(100), nullable=False)
    school: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    district: Mapped[str | None] = mapped_column(String(100))
    address_detail: Mapped[str | None] = mapped_column(Text)
    student_id_card_url: Mapped[str | None] = mapped_column(String(500))
    cv_url: Mapped[str | None] = mapped_column(String(500))
    avatar_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    bio: Mapped[str | None] = mapped_column(Text)
    avg_rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_ratings: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=func.now())

    # Relationships
    subjects: Mapped[list["UserSubject"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    hosted_rooms: Mapped[list["Room"]] = relationship(back_populates="host")
    # ... các relationship khác
```

### 2.2. Alembic Migration

Cấu hình `alembic/env.py`:
- Import tất cả models từ `app.models`
- Dùng `target_metadata = Base.metadata`
- Config cho async PostgreSQL

Tạo migration:
```bash
alembic revision --autogenerate -m "create_all_tables"
```

### 2.3. Seed Data

Tạo script `backend/app/seed.py` để seed `room_category`:
```python
CATEGORIES = [
    {"name": "Toán học", "icon": "📐", "color": "#FF6B6B", "display_order": 1},
    {"name": "Lập trình", "icon": "💻", "color": "#4ECDC4", "display_order": 2},
    {"name": "Ngoại ngữ", "icon": "🌍", "color": "#45B7D1", "display_order": 3},
    {"name": "Khoa học tự nhiên", "icon": "🔬", "color": "#96CEB4", "display_order": 4},
    {"name": "Kinh tế", "icon": "📊", "color": "#FECA57", "display_order": 5},
    {"name": "Y - Dược", "icon": "⚕️", "color": "#FF9FF3", "display_order": 6},
    {"name": "Luật", "icon": "⚖️", "color": "#54A0FF", "display_order": 7},
    {"name": "Kỹ thuật", "icon": "⚙️", "color": "#5F27CD", "display_order": 8},
    {"name": "Nghệ thuật", "icon": "🎨", "color": "#FF6348", "display_order": 9},
    {"name": "Khác", "icon": "📚", "color": "#A0A0A0", "display_order": 10},
]
```

Tích hợp seed vào CLI hoặc chạy riêng: `python -m app.seed`

## Tiêu chí hoàn thành

- [ ] Tất cả 10 bảng đã khai báo đúng theo schema doc
- [ ] Alembic migration tạo thành công, `alembic upgrade head` chạy pass
- [ ] `alembic downgrade base` rollback sạch
- [ ] Seed script chạy thành công, 10 categories được insert
- [ ] Kiểm tra DB thủ công: tất cả indexes, unique constraints, foreign keys đúng
- [ ] Import `from app.models import *` không lỗi circular import
