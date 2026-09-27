import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.room import Room


class Rating(Base):
    """Bảng rating — Đánh giá bạn học (1–5 sao) sau khi rời phòng học trực tuyến."""
    __tablename__ = "rating"
    __table_args__ = (
        CheckConstraint("stars >= 1 AND stars <= 5", name="chk_rating_stars"),
        UniqueConstraint("rater_id", "ratee_id", "room_id", name="uq_rating_per_room"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rater_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ratee_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("room.id", ondelete="CASCADE"), nullable=False, index=True
    )
    stars: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Quan hệ
    rater: Mapped["User"] = relationship(
        "User", foreign_keys=[rater_id], back_populates="ratings_given"
    )
    ratee: Mapped["User"] = relationship(
        "User", foreign_keys=[ratee_id], back_populates="ratings_received"
    )
    room: Mapped["Room"] = relationship("Room", back_populates="ratings")
