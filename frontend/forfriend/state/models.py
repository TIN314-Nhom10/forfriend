"""Pydantic BaseModel cho các đối tượng lưu trong State và render qua rx.foreach."""
from pydantic import BaseModel


class PostItem(BaseModel):
    id: str = ""
    title: str = ""
    content: str = ""
    author_id: str = ""
    author_name: str = "Student"
    author_avatar_id: int = 1
    author_school: str = "Đại học"
    author_rating: float = 5.0
    author_total_ratings: int = 0
    match_score: float = 0.85
    match_pct: str = "85%"
    tags: list[str] = []
    is_online: bool = True
    location: str = "Online"
    created_at: str = ""
    is_mine: bool = False


class RoomItem(BaseModel):
    id: str = ""
    room_code: str = "ZONE-01"
    title: str = "Study Room"
    topic: str = ""
    category_name: str = "Chung"
    category_icon: str = "🎮"
    host_id: str = ""
    host_name: str = "Host"
    host_avatar_id: int = 1
    current_participants: int = 1
    max_participants: int = 6
    is_full: bool = False
    is_my_room: bool = False


class CategoryItem(BaseModel):
    id: str = ""
    name: str = "Chung"
    code: str = "general"
    icon: str = "🎮"


class FriendItem(BaseModel):
    friendship_id: str = ""
    user_id: str = ""
    name: str = "Student"
    avatar_id: int = 1
    school: str = ""
    rating: float = 5.0
    is_online: bool = False
    since: str = ""


class FriendRequestItem(BaseModel):
    friendship_id: str = ""
    user_id: str = ""
    name: str = "Student"
    avatar_id: int = 1
    school: str = ""


class MessageItem(BaseModel):
    id: str = ""
    sender_id: str = ""
    receiver_id: str = ""
    content: str = ""
    is_mine: bool = False
    is_read: bool = False
    created_at: str = ""


class ReviewItem(BaseModel):
    stars: int = 5
    comment: str = ""
    reviewer_name: str = "Student"
    reviewer_avatar_id: int = 1
    created_at: str = ""


class TeammateItem(BaseModel):
    id: str = ""
    name: str = "Student"
    avatar_id: int = 1
    school: str = ""


class KnockRequestItem(BaseModel):
    id: str = ""
    user_id: str = ""
    name: str = "Student"
    avatar_id: int = 1
    school: str = ""
