import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.room import UserBrief


class FriendResponse(BaseModel):
    """Thông tin bạn bè kèm trạng thái Online/Offline."""
    model_config = ConfigDict(from_attributes=True)

    friendship_id: uuid.UUID
    friend: UserBrief
    is_online: bool = False
    since: datetime


class FriendRequestResponse(BaseModel):
    """Thông tin lời mời kết bạn đang chờ phản hồi."""
    model_config = ConfigDict(from_attributes=True)

    friendship_id: uuid.UUID
    from_user: UserBrief
    created_at: datetime


class FriendActionResponse(BaseModel):
    """Phản hồi sau khi thực hiện thao tác kết bạn (chấp nhận/từ chối/hủy bạn)."""
    message: str
    status: str


class MessageCreateRequest(BaseModel):
    """Payload gửi tin nhắn mới."""
    content: str = Field(..., min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    """Chi tiết một tin nhắn 1-1."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    content: str
    is_mine: bool = False
    is_read: bool = False
    created_at: datetime
    read_at: Optional[datetime] = None


class ConversationResponse(BaseModel):
    """Thông tin cuộc trò chuyện với một người bạn."""
    friend: UserBrief
    is_online: bool = False
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0


class MessageListResponse(BaseModel):
    """Danh sách tin nhắn trong cuộc trò chuyện (cursor pagination)."""
    items: List[MessageResponse]
    has_more: bool = False
    total: Optional[int] = None
