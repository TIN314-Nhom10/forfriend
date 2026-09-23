# Task 02 — Database Models & Initialization (SQLite Edition)

## Mục tiêu
Tạo tất cả 10 SQLAlchemy models theo schema đã thiết kế trong `docs/02-database-schema.md`, đảm bảo tương thích 100% với SQLite async (`aiosqlite`), và viết script `init_db.py` tự tạo bảng và seed data ban đầu trong 1 lệnh duy nhất.

## Phụ thuộc
- Task 01 (Project Setup) — cần `database.py`, `Base`

## Tham chiếu
- [02-database-schema.md](../02-database-schema.md) — Schema chi tiết cho từng bảng

## Yêu cầu chi tiết

### 2.1. SQLAlchemy Models (Tương thích SQLite)

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

**Quy ước chung cho mọi model tương thích SQLite:**
- Dùng cú pháp `Mapped` và `mapped_column` chuẩn của SQLAlchemy 2.0.
- Khóa chính UUID: Dùng `sqlalchemy.types.Uuid(as_uuid=True)` kèm `default=uuid.uuid4`. Chuẩn này tương thích hoàn hảo với SQLite (lưu string 36 ký tự) và chuyển đổi mượt mà sang `uuid.UUID` trong Python.
- Timestamps: Dùng `server_default=func.now()` và `onupdate=func.now()`.
- Relationship khai báo với `back_populates` đầy đủ 2 chiều.
- Type hints bắt buộc cho tất cả columns.

**Ví dụ mẫu cho `backend/app/models/user.py`:**
```python
import uuid
from datetime import date, datetime
from sqlalchemy import String, Integer, Float, Boolean, Date, Text, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    """Bảng user — thông tin sinh viên."""
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
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
```

---

### 2.2. Script Khởi Tạo & Seed Dữ Liệu (`init_db.py`)

Tạo file `backend/app/init_db.py` để người chấm bài / developer có thể khởi tạo database và dữ liệu mẫu bất cứ lúc nào:

```python
import asyncio
from app.database import engine, Base, AsyncSessionLocal
from app.models.room import RoomCategory
import app.models  # Nạp tất cả 10 models

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

async def init_database():
    print("🚀 Initializing SQLite database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully.")

    async with AsyncSessionLocal() as session:
        # Seed categories nếu chưa có
        for cat_data in CATEGORIES:
            cat = RoomCategory(**cat_data)
            session.add(cat)
        try:
            await session.commit()
            print(f"✅ Seeded {len(CATEGORIES)} room categories.")
        except Exception:
            await session.rollback()
            print("ℹ️ Categories already exist or skipped.")

    await engine.dispose()
    print("🎉 Database setup complete! File: forfriend.db")

if __name__ == "__main__":
    asyncio.run(init_database())
```

**Cách chạy:**
```bash
cd backend
python -m app.init_db
```

---

### 2.3. Tự Động Khởi Tạo Khi Start Server (FastAPI Lifespan)

Trong `backend/app/main.py`, sự kiện `lifespan` sẽ tự động gọi tạo bảng nếu file `forfriend.db` chưa tồn tại, giúp giảng viên chỉ cần chạy lệnh uvicorn là database tự hoạt động.

*(Tùy chọn mở rộng)*: Vẫn có thể cấu hình Alembic nếu muốn làm bài tập nâng cao về Database Migrations:
```bash
alembic revision --autogenerate -m "create_initial_sqlite_schema"
alembic upgrade head
```

---

## Tiêu chí hoàn thành

- [ ] Tất cả 10 bảng đã khai báo đúng theo schema doc và tương thích SQLite (`Uuid` type)
- [ ] Lệnh `python -m app.init_db` chạy thành công không sinh lỗi
- [ ] File `backend/forfriend.db` xuất hiện và chứa đầy đủ 10 bảng cùng dữ liệu mẫu categories
- [ ] Import `from app.models import *` không bị lỗi circular import
- [ ] Không phụ thuộc vào Docker hay PostgreSQL server bên ngoài
