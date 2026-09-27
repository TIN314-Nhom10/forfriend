import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.room import Room, RoomParticipant
    from app.models.rating import Rating
    from app.models.friendship import Friendship
    from app.models.message import Message


class User(Base):
    """Bảng user — Thông tin tài khoản sinh viên / Hero Profile."""
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    major: Mapped[str] = mapped_column(String(100), nullable=False)
    school: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    student_id_card_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cv_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    avatar_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avg_rating: Mapped[float] = mapped_column(Float, default=0.0)
    total_ratings: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)

    # Quan hệ
    subjects: Mapped[List["UserSubject"]] = relationship(
        "UserSubject", back_populates="user", cascade="all, delete-orphan"
    )
    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan"
    )
    hosted_rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="host"
    )
    room_participations: Mapped[List["RoomParticipant"]] = relationship(
        "RoomParticipant", back_populates="user", cascade="all, delete-orphan"
    )
    ratings_given: Mapped[List["Rating"]] = relationship(
        "Rating", foreign_keys="Rating.rater_id", back_populates="rater"
    )
    ratings_received: Mapped[List["Rating"]] = relationship(
        "Rating", foreign_keys="Rating.ratee_id", back_populates="ratee"
    )
    friendships_requested: Mapped[List["Friendship"]] = relationship(
        "Friendship", foreign_keys="Friendship.requester_id", back_populates="requester"
    )
    friendships_received: Mapped[List["Friendship"]] = relationship(
        "Friendship", foreign_keys="Friendship.addressee_id", back_populates="addressee"
    )
    sent_messages: Mapped[List["Message"]] = relationship(
        "Message", foreign_keys="Message.sender_id", back_populates="sender"
    )
    received_messages: Mapped[List["Message"]] = relationship(
        "Message", foreign_keys="Message.receiver_id", back_populates="receiver"
    )


class UserSubject(Base):
    """Bảng user_subject — Môn học sinh viên đang theo học hoặc cần tìm bạn."""
    __tablename__ = "user_subject"
    __table_args__ = (
        UniqueConstraint("user_id", "subject_name", name="uq_user_subject"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Quan hệ
    user: Mapped["User"] = relationship("User", back_populates="subjects")
