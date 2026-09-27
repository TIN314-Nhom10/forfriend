from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    TokenResponse,
    UserBrief,
)
from app.services.auth_service import auth_service
from app.utils.dependencies import get_current_user, limiter

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản Hero mới",
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Đăng ký tài khoản sinh viên (Hero) mới:
    - Kiểm tra email chưa tồn tại
    - Mật khẩu tối thiểu 8 ký tự, có ít nhất 1 chữ in hoa và 1 chữ số
    - Chọn 1 trong 15 avatar chibi đại diện
    - Trả về cặp access token (60 phút) & refresh token (7 ngày)
    """
    return await auth_service.register_user(db, data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Đăng nhập tài khoản Hero",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Đăng nhập bằng email và mật khẩu:
    - Xác thực mật khẩu qua bcrypt
    - Cấp access token và refresh token
    """
    return await auth_service.login_user(db, data)


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    summary="Cấp lại access token qua refresh token",
)
@limiter.limit("30/minute")
async def refresh_token(
    request: Request,
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Cấp mới access token khi token cũ đã hết hạn.
    """
    return await auth_service.refresh_access_token(db, data)


@router.get(
    "/me",
    response_model=UserBrief,
    summary="Lấy thông tin tài khoản hiện tại",
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Lấy thông tin Hero đang đăng nhập (yêu cầu Authorization: Bearer <token>).
    """
    return UserBrief.model_validate(current_user)
