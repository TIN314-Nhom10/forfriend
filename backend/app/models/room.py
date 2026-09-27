import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.rating import Rating


class RoomCategory(Base):
    """Bảng room_category — Danh mục phân loại các phòng học (Adventure Zones)."""
    __tablename__ = "room_category"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # Emoji hoặc icon code
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # Mã màu hex (e.g. #FF6B6B)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

    # Quan hệ
    rooms: Mapped[List["Room"]] = relationship("Room", back_populates="category")


class Room(Base):
    """Bảng room — Phòng học ảo video call (Lobby & Video Room)."""
    __tablename__ = "room"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    host_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    topic: Mapped[str] = mapped_column(String(200), nullable=False)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("room_category.id", ondelete="SET NULL"), nullable=True, index=True
    )
    room_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="waiting", index=True)  # waiting | active | closed
    max_participants: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    current_participants: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Quan hệ
    host: Mapped["User"] = relationship("User", back_populates="hosted_rooms")
    category: Mapped[Optional["RoomCategory"]] = relationship("RoomCategory", back_populates="rooms")
    participants: Mapped[List["RoomParticipant"]] = relationship(
        "RoomParticipant", back_populates="room", cascade="all, delete-orphan"
    )
    ratings: Mapped[List["Rating"]] = relationship(
        "Rating", back_populates="room", cascade="all, delete-orphan"
    )


class RoomParticipant(Base):
    """Bảng room_participant — Quản lý người tham gia phòng và phê duyệt của Host."""
    __tablename__ = "room_participant"
    __table_args__ = (
        UniqueConstraint("room_id", "user_id", name="uq_room_participant"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("room.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )  # pending | accepted | rejected | left
    requested_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    joined_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Quan hệ
    room: Mapped["Room"] = relationship("Room", back_populates="participants")
    user: Mapped["User"] = relationship("User", back_populates="room_participations")
