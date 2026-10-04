import uuid
from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class UserBrief(BaseModel):
    """Thông tin tóm tắt của Hero (Host / Participant)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    avatar_id: int = 1
    school: Optional[str] = None
    avg_rating: float = 0.0


class RoomCategoryResponse(BaseModel):
    """Thông tin danh mục phân khu phòng học (Adventure Zone)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    icon: Optional[str] = None
    color: Optional[str] = None
    display_order: int = 0
    active_rooms_count: Optional[int] = 0


class ParticipantResponse(BaseModel):
    """Thông tin người tham gia phòng học."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    room_id: uuid.UUID
    user: UserBrief
    status: str  # pending | accepted | rejected | left
    requested_at: datetime
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None


class RoomCreate(BaseModel):
    """Payload tạo phòng học mới."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Tên phòng học")
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Alias cho Tên phòng học")
    topic: str = Field(..., min_length=1, max_length=200, description="Chủ đề môn học")
    category_id: uuid.UUID = Field(..., description="ID phân khu danh mục môn học")
    max_participants: int = Field(default=10, ge=2, le=20, description="Số lượng thành viên tối đa (2-20)")

    @model_validator(mode="before")
    @classmethod
    def check_name_or_title(cls, data: Any):
        if isinstance(data, dict):
            if not data.get("name") and data.get("title"):
                data["name"] = data["title"]
            elif not data.get("title") and data.get("name"):
                data["title"] = data["name"]
        return data


class RoomResponse(BaseModel):
    """Thông tin tóm tắt của phòng học."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    room_code: str
    topic: str
    category: Optional[RoomCategoryResponse] = None
    host: UserBrief
    status: str  # waiting | active | closed
    max_participants: int
    current_participants: int
    created_at: datetime
    closed_at: Optional[datetime] = None


class RoomDetailResponse(RoomResponse):
    """Thông tin chi tiết phòng kèm danh sách participants."""
    participants: List[ParticipantResponse] = Field(default_factory=list)


class RoomListResponse(BaseModel):
    """Danh sách phòng học có phân trang (Lobby)."""
    items: List[RoomResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class JoinRequestResponse(BaseModel):
    """Kết quả gửi yêu cầu xin vào phòng."""
    participant_id: uuid.UUID
    status: str = "pending"
    message: str = "Yêu cầu đã được gửi tới host"


class ApproveResponse(BaseModel):
    """Kết quả duyệt yêu cầu tham gia phòng."""
    status: str = "accepted"
    livekit_token: Optional[str] = None
    livekit_url: Optional[str] = None


class RoomTokenResponse(BaseModel):
    """Thông tin token LiveKit để kết nối phòng học WebRTC."""
    room_id: uuid.UUID
    room_code: str
    livekit_token: str
    livekit_url: str
    token: Optional[str] = None
    url: Optional[str] = None
    is_host: Optional[bool] = False
