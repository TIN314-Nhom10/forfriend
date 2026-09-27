import uuid
from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserSubject
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    TokenResponse,
    UserBrief,
)
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    sanitize_text,
    verify_password,
)


class AuthService:
    """Business Logic Service phụ trách Đăng ký, Đăng nhập và Token."""

    @staticmethod
    async def register_user(db: AsyncSession, data: RegisterRequest) -> TokenResponse:
        email = data.email.lower().strip()

        # Kiểm tra email đã đăng ký chưa
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        if result.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email này đã được sử dụng bởi một tài khoản khác",
            )

        # Băm mật khẩu và làm sạch dữ liệu văn bản chống XSS
        password_hash = hash_password(data.password)
        dob = data.date_of_birth or date(2003, 1, 1)
        user_major = sanitize_text(data.major) if data.major else "General"

        new_user = User(
            email=email,
            password_hash=password_hash,
            name=sanitize_text(data.name) or data.name,
            date_of_birth=dob,
            major=user_major or "General",
            school=sanitize_text(data.school) or data.school,
            city=sanitize_text(data.city) or data.city,
            district=sanitize_text(data.district),
            address_detail=sanitize_text(data.address_detail),
            avatar_id=data.avatar_id,
            bio=sanitize_text(data.bio),
        )
        db.add(new_user)
        await db.flush()

        # Thêm danh sách môn học nếu có
        for subj in set(data.subjects):
            clean_subj = sanitize_text(subj)
            if clean_subj:
                user_subject = UserSubject(user_id=new_user.id, subject_name=clean_subj)
                db.add(user_subject)

        await db.commit()
        await db.refresh(new_user)

        # Cấp token
        token_data = {"sub": str(new_user.id), "email": new_user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserBrief.model_validate(new_user),
        )

    @staticmethod
    async def login_user(db: AsyncSession, data: LoginRequest) -> TokenResponse:
        email = data.email.lower().strip()

        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không chính xác",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản này đã bị vô hiệu hóa",
            )

        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserBrief.model_validate(user),
        )

    @staticmethod
    async def refresh_access_token(
        db: AsyncSession, data: RefreshRequest
    ) -> RefreshResponse:
        unauthorized_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token không hợp lệ hoặc đã hết hạn",
        )

        try:
            payload = decode_token(data.refresh_token)
            if payload.get("type") != "refresh":
                raise unauthorized_exception

            user_id_str = payload.get("sub")
            if not user_id_str:
                raise unauthorized_exception

            user_id = uuid.UUID(user_id_str)
        except (JWTError, ValueError):
            raise unauthorized_exception

        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None or not user.is_active:
            raise unauthorized_exception

        new_access_token = create_access_token(
            {"sub": str(user.id), "email": user.email}
        )

        return RefreshResponse(access_token=new_access_token)


auth_service = AuthService()
