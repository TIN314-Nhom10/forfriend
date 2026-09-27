"""
Script khởi tạo database SQLite và nạp dữ liệu mẫu ban đầu (Seed Data).
Chạy trực tiếp:
    cd backend
    python -m app.init_db
"""
import asyncio
import logging
from datetime import date
import uuid
from sqlalchemy import select
from app.database import AsyncSessionLocal, Base, engine
from app.models.room import RoomCategory
from app.models.user import User
from app.models.post import Post, PostTag
from app.utils.security import hash_password
import app.models  # Nạp tất cả 10 models

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Danh sách 10 chủ đề phòng học chuẩn (Adventure Zones)
SEED_CATEGORIES = [
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

DEMO_USERS = [
    {
        "email": "liam@forfriend.local",
        "name": "Liam M.",
        "password": "Password123!",
        "date_of_birth": date(2003, 5, 15),
        "major": "Computer Science",
        "school": "Gaming headphones",
        "city": "Hà Nội",
        "avatar_id": 1,
        "bio": "Bio, cute chibi cat, catan, gaming headset, and master unique study partners.",
        "avg_rating": 5.0,
        "total_ratings": 18,
        "post_title": "Python Project: AI Chatbot",
        "post_desc": "Python project of : AI Chatbot in Python for a term project, know about natural conversations.",
        "post_tags": ["Python", "AI", "Collaborating"],
    },
    {
        "email": "chloe@forfriend.local",
        "name": "Chloe T.",
        "password": "Password123!",
        "date_of_birth": date(2004, 8, 20),
        "major": "Mathematics",
        "school": "Reading",
        "city": "Hà Nội",
        "avatar_id": 2,
        "bio": "Reading study partners to find reviewer channels for math and calculus ideas.",
        "avg_rating": 4.9,
        "total_ratings": 14,
        "post_title": "Math Prep: Calculus II",
        "post_desc": "Reading study partners to find reviewer channels for math and calculus ideas.",
        "post_tags": ["Math", "Calculus", "Evening"],
    },
    {
        "email": "ben@forfriend.local",
        "name": "Ben S.",
        "password": "Password123!",
        "date_of_birth": date(2003, 1, 10),
        "major": "UI/UX Design",
        "school": "Designing",
        "city": "Hà Nội",
        "avatar_id": 3,
        "bio": "UI/UX Design review is brand new design compartments, design and creative.",
        "avg_rating": 4.8,
        "total_ratings": 11,
        "post_title": "UI/UX Design Review",
        "post_desc": "UI/UX Design review is brand new design compartments, design and creative.",
        "post_tags": ["Design", "Figma", "Creative"],
    },
    {
        "email": "anya@forfriend.local",
        "name": "Anya L.",
        "password": "Password123!",
        "date_of_birth": date(2003, 11, 25),
        "major": "Literature & History",
        "school": "Writing",
        "city": "Hà Nội",
        "avatar_id": 4,
        "bio": "History essay and descriptions to students' problemic history, mister combination.",
        "avg_rating": 5.0,
        "total_ratings": 16,
        "post_title": "History Essay",
        "post_desc": "History essay and descriptions to students' problemic history, mister combination.",
        "post_tags": ["History", "Research", "Daytime"],
    },
    {
        "email": "nguyenvana@ftu.edu.vn",
        "name": "Nguyễn Văn A",
        "password": "Password123!",
        "date_of_birth": date(2003, 5, 15),
        "major": "Kinh tế Quốc tế",
        "school": "Đại học Ngoại Thương Hà Nội",
        "city": "Hà Nội",
        "avatar_id": 1,
        "bio": "Sinh viên năm 3 FTU, đam mê Python, AI và Web development.",
        "avg_rating": 4.9,
        "total_ratings": 12,
        "post_title": "Python & Data Analytics Group",
        "post_desc": "Tìm bạn cùng học Python & phân tích dữ liệu kinh tế lượng.",
        "post_tags": ["Python", "KinhTe", "HocNhom"],
    },
    {
        "email": "tranthib@neu.edu.vn",
        "name": "Trần Thị B",
        "password": "Password123!",
        "date_of_birth": date(2004, 8, 20),
        "major": "Tài chính Doanh nghiệp",
        "school": "Đại học Kinh Tế Quốc Dân",
        "city": "Hà Nội",
        "avatar_id": 2,
        "bio": "Thích học nhóm giải toán xác suất thống kê và kinh tế lượng.",
        "avg_rating": 4.8,
        "total_ratings": 8,
        "post_title": "Ôn thi Xác Suất Thống Kê",
        "post_desc": "Thích học nhóm giải toán xác suất thống kê và kinh tế lượng.",
        "post_tags": ["Toan", "NEU", "HocTap"],
    },
]


async def seed_categories() -> int:
    """Nạp danh sách room categories nếu chưa tồn tại."""
    added_count = 0
    async with AsyncSessionLocal() as session:
        for cat_data in SEED_CATEGORIES:
            stmt = select(RoomCategory).where(RoomCategory.name == cat_data["name"])
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            if not existing:
                cat = RoomCategory(**cat_data)
                session.add(cat)
                added_count += 1
        if added_count > 0:
            await session.commit()
            logger.info(f"Đã nạp thành công {added_count} danh mục phòng học.")
        else:
            logger.info("Tất cả danh mục phòng học đã tồn tại đầy đủ trong database.")
    return added_count


async def seed_demo_users() -> None:
    """Nạp các tài khoản demo có sẵn phục vụ kiểm thử nhanh."""
    async with AsyncSessionLocal() as session:
        for u in DEMO_USERS:
            stmt = select(User).where(User.email == u["email"])
            res = await session.execute(stmt)
            user_obj = res.scalar_one_or_none()
            if not user_obj:
                new_u = User(
                    id=uuid.uuid4(),
                    email=u["email"],
                    password_hash=hash_password(u["password"]),
                    name=u["name"],
                    date_of_birth=u["date_of_birth"],
                    major=u["major"],
                    school=u["school"],
                    city=u["city"],
                    avatar_id=u["avatar_id"],
                    bio=u["bio"],
                    avg_rating=u["avg_rating"],
                    total_ratings=u["total_ratings"],
                    is_active=True,
                )
                session.add(new_u)
                await session.flush()

                # Tạo quest mẫu cho user theo mockup
                title = u.get("post_title", f"{u['major']} Study Quest")
                desc = u.get("post_desc", f"Tìm bạn cùng học nhóm {u['major']} & Ôn thi cuối kỳ môn học.")
                post = Post(
                    id=uuid.uuid4(),
                    author_id=new_u.id,
                    content=f"[{title}] {desc}",
                    study_type="online",
                    is_active=True,
                )
                session.add(post)
                await session.flush()
                tags = u.get("post_tags", ["Python", "HocNhom", "DoAn"])
                for tag_name in tags:
                    session.add(PostTag(post_id=post.id, tag_name=tag_name))

                logger.info(f"Đã tạo user demo: {u['email']} / Password123!")
            else:
                user_obj.password_hash = hash_password(u["password"])
        await session.commit()
        logger.info("✅ Hoàn tất kiểm tra / nạp tài khoản demo.")


async def init_database() -> None:
    logger.info("🚀 Bắt đầu khởi tạo database SQLite (forfriend.db)...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Tạo thành công 10 bảng trong database.")

    await seed_categories()
    await seed_demo_users()
    await engine.dispose()
    logger.info("🎉 Database setup complete! (0% Docker / Zero external dependencies)")


if __name__ == "__main__":
    asyncio.run(init_database())
