import secrets
import string
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.room import Room


def generate_room_code(length: int = 6) -> str:
    """Tạo mã phòng ngẫu nhiên gồm chữ in hoa và chữ số (ví dụ: 'XK3M7P')."""
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


async def get_unique_room_code(db: AsyncSession, length: int = 6) -> str:
    """Tạo mã phòng và kiểm tra tính duy nhất trong database."""
    for _ in range(10):
        code = generate_room_code(length)
        result = await db.execute(select(Room.id).where(Room.room_code == code))
        if result.scalar_one_or_none() is None:
            return code
    # Fallback tăng độ dài nếu trùng nhiều lần
    return generate_room_code(length + 2)
