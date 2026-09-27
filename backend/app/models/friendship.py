import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Friendship(Base):
    """Bảng friendship — Quản lý quan hệ kết bạn và trạng thái mời kết bạn giữa sinh viên."""
    __tablename__ = "friendship"
    __table_args__ = (
        UniqueConstraint("requester_id", "addressee_id", name="uq_friendship_pair"),
        CheckConstraint("requester_id != addressee_id", name="chk_not_self_friend"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    addressee_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )  # pending | accepted | rejected | blocked
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Quan hệ
    requester: Mapped["User"] = relationship(
        "User", foreign_keys=[requester_id], back_populates="friendships_requested"
    )
    addressee: Mapped["User"] = relationship(
        "User", foreign_keys=[addressee_id], back_populates="friendships_received"
    )
