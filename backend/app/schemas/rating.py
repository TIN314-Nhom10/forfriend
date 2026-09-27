import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.room import UserBrief


class RatingCreate(BaseModel):
    """Payload gửi đánh giá bạn học sau buổi học."""
    ratee_id: uuid.UUID = Field(..., description="ID của người được đánh giá")
    room_id: uuid.UUID = Field(..., description="ID của phòng học đã tham gia")
    stars: int = Field(..., ge=1, le=5, description="Số sao đánh giá từ 1 đến 5")
    comment: Optional[str] = Field(None, max_length=500, description="Nhận xét chi tiết")


class RatingResponse(BaseModel):
    """Chi tiết lượt đánh giá."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    rater: UserBrief
    ratee: UserBrief
    room_id: uuid.UUID
    stars: int
    comment: Optional[str] = None
    created_at: datetime


class UserRatingsResponse(BaseModel):
    """Danh sách các lượt đánh giá của một Hero."""
    items: List[RatingResponse]
    total: int
    avg_rating: float
    page: int
    per_page: int
    total_pages: int
