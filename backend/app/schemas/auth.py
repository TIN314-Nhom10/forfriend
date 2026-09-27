import re
import uuid
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBrief(BaseModel):
    """Thông tin tóm tắt của Hero (User) trả về sau khi xác thực."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: str
    avatar_id: int
    school: str
    major: str


class RegisterRequest(BaseModel):
    """Yêu cầu đăng ký tài khoản sinh viên mới."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mật khẩu tối thiểu 8 ký tự, có ít nhất 1 chữ hoa và 1 số")
    name: str = Field(..., min_length=2, max_length=100, description="Họ và tên sinh viên")
    date_of_birth: Optional[date] = Field(default=None, description="Ngày sinh")
    major: Optional[str] = Field(default="General", max_length=100, description="Chuyên ngành học")
    school: str = Field(..., min_length=2, max_length=200, description="Trường Đại học/Cao đẳng")
    city: str = Field(..., min_length=2, max_length=100, description="Tỉnh/Thành phố sinh sống")
    district: Optional[str] = Field(default=None, max_length=100)
    address_detail: Optional[str] = Field(default=None)
    avatar_id: int = Field(default=1, ge=1, le=15, description="ID avatar từ 1 đến 15")
    bio: Optional[str] = Field(default=None, description="Đôi dòng giới thiệu bản thân")
    subjects: List[str] = Field(default_factory=list, description="Danh sách các môn học quan tâm")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Mật khẩu phải chứa ít nhất 8 ký tự")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Mật khẩu phải chứa ít nhất 1 chữ in hoa")
        if not re.search(r"[0-9]", v):
            raise ValueError("Mật khẩu phải chứa ít nhất 1 chữ số")
        return v


class LoginRequest(BaseModel):
    """Yêu cầu đăng nhập."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Phản hồi sau khi đăng ký hoặc đăng nhập thành công."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserBrief


class RefreshRequest(BaseModel):
    """Yêu cầu cấp mới access token qua refresh token."""
    refresh_token: str


class RefreshResponse(BaseModel):
    """Phản hồi token mới."""
    access_token: str
    token_type: str = "bearer"
