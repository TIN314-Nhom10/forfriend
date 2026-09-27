import uuid
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class UserProfile(BaseModel):
    """Hồ sơ cá nhân đầy đủ của Hero (Current User)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str
    date_of_birth: date
    major: str
    school: str
    city: str
    district: Optional[str] = None
    address_detail: Optional[str] = None
    student_id_card_url: Optional[str] = None
    cv_url: Optional[str] = None
    is_verified: bool = False
    avatar_id: int
    bio: Optional[str] = None
    avg_rating: float
    total_ratings: int
    subjects: List[str] = Field(default_factory=list)
    created_at: datetime


class UserPublic(BaseModel):
    """Hồ sơ công khai của Hero hiển thị cho người khác xem."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    school: str
    major: str
    city: str
    avatar_id: int
    bio: Optional[str] = None
    avg_rating: float
    total_ratings: int
    subjects: List[str] = Field(default_factory=list)


class UserUpdate(BaseModel):
    """Payload cập nhật thông tin Hero (chỉ truyền các trường cần đổi)."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    major: Optional[str] = Field(None, min_length=2, max_length=100)
    school: Optional[str] = Field(None, min_length=2, max_length=200)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    district: Optional[str] = None
    address_detail: Optional[str] = None
    avatar_id: Optional[int] = Field(None, ge=1, le=15, description="ID avatar chibi từ 1 đến 15")
    bio: Optional[str] = None
    subjects: Optional[List[str]] = None


class FileUploadResponse(BaseModel):
    """Phản hồi đường dẫn file sau khi upload thành công."""
    url: str
    message: Optional[str] = None
    verification: Optional[dict] = None
