import uuid
from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class AuthorBrief(BaseModel):
    """Thông tin tóm tắt của tác giả bài đăng (Hero)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    avatar_id: int
    school: str
    avg_rating: float


class PostCreate(BaseModel):
    """Payload tạo bài đăng tìm bạn học mới (Quest)."""
    content: str = Field(..., min_length=10, max_length=2000, description="Nội dung bài đăng")
    study_type: Literal["online", "offline"] = Field(..., description="Hình thức học: online hoặc offline")
    location: Optional[str] = Field(None, max_length=200, description="Địa điểm học (bắt buộc cho offline)")
    preferred_school: Optional[str] = Field(None, max_length=200, description="Ưu tiên trường học")
    study_date: Optional[datetime] = Field(None, description="Thời gian dự kiến học")
    max_people: int = Field(default=5, ge=2, le=20, description="Số lượng người tối đa (2-20)")
    tags: List[str] = Field(default_factory=list, max_length=5, description="Tối đa 5 tags chủ đề môn học")

    @model_validator(mode="after")
    def validate_offline_location(self) -> "PostCreate":
        if self.study_type == "offline" and not (self.location and self.location.strip()):
            raise ValueError("Địa điểm (location) là bắt buộc đối với hình thức học offline")
        return self


class PostUpdate(BaseModel):
    """Payload cập nhật bài đăng."""
    content: Optional[str] = Field(None, min_length=10, max_length=2000)
    study_type: Optional[Literal["online", "offline"]] = None
    location: Optional[str] = Field(None, max_length=200)
    preferred_school: Optional[str] = Field(None, max_length=200)
    study_date: Optional[datetime] = None
    max_people: Optional[int] = Field(None, ge=2, le=20)
    tags: Optional[List[str]] = Field(None, max_length=5)

    @model_validator(mode="after")
    def validate_update_offline_location(self) -> "PostUpdate":
        if self.study_type == "offline" and self.location is not None and not self.location.strip():
            raise ValueError("Địa điểm không được để trống khi học offline")
        return self


class PostResponse(BaseModel):
    """Chi tiết bài đăng tìm bạn học trả về cho client."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content: str
    study_type: str
    location: Optional[str] = None
    preferred_school: Optional[str] = None
    study_date: Optional[datetime] = None
    max_people: int
    author: AuthorBrief
    tags: List[str] = Field(default_factory=list)
    relevance_score: Optional[float] = None
    created_at: datetime


class PostListResponse(BaseModel):
    """Phản hồi danh sách bài đăng có phân trang."""
    items: List[PostResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
