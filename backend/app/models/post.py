import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Post(Base):
    """Bảng post — Bài đăng tìm bạn học nhóm Offline/Online (Quest)."""
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    study_type: Mapped[str] = mapped_column(String(10), nullable=False)  # "online" | "offline"
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    preferred_school: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    study_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    max_people: Mapped[int] = mapped_column(Integer, default=5)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    # Quan hệ
    author: Mapped["User"] = relationship("User", back_populates="posts")
    tags: Mapped[List["PostTag"]] = relationship(
        "PostTag", back_populates="post", cascade="all, delete-orphan"
    )


class PostTag(Base):
    """Bảng post_tag — Tag chủ đề môn học gắn với bài đăng (ví dụ: 'giai-tich', 'python')."""
    __tablename__ = "post_tag"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("post.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tag_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Quan hệ
    post: Mapped["Post"] = relationship("Post", back_populates="tags")
