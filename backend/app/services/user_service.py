import uuid
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User, UserSubject
from app.schemas.user import UserProfile, UserPublic, UserUpdate
from app.utils.security import sanitize_text


class UserService:
    """Business Logic Service phụ trách quản lý hồ sơ Hero (User Profile)."""

    @staticmethod
    async def get_profile(db: AsyncSession, user_id: uuid.UUID) -> UserProfile:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.subjects))
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy thông tin người dùng",
            )

        subjects_list = [s.subject_name for s in user.subjects]
        return UserProfile(
            id=user.id,
            email=user.email,
            name=user.name,
            date_of_birth=user.date_of_birth,
            major=user.major,
            school=user.school,
            city=user.city,
            district=user.district,
            address_detail=user.address_detail,
            student_id_card_url=user.student_id_card_url,
            cv_url=user.cv_url,
            is_verified=bool(user.student_id_card_url),
            avatar_id=user.avatar_id,
            bio=user.bio,
            avg_rating=user.avg_rating,
            total_ratings=user.total_ratings,
            subjects=subjects_list,
            created_at=user.created_at,
        )

    @staticmethod
    async def get_public_profile(db: AsyncSession, user_id: uuid.UUID) -> UserPublic:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.subjects))
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bạn học này hoặc tài khoản đã bị khóa",
            )

        subjects_list = [s.subject_name for s in user.subjects]
        return UserPublic(
            id=user.id,
            name=user.name,
            school=user.school,
            major=user.major,
            city=user.city,
            avatar_id=user.avatar_id,
            bio=user.bio,
            avg_rating=user.avg_rating,
            total_ratings=user.total_ratings,
            subjects=subjects_list,
        )

    @staticmethod
    async def update_profile(
        db: AsyncSession, current_user: User, data: UserUpdate
    ) -> UserProfile:
        # Cập nhật các trường văn bản nếu có truyền lên
        if data.name is not None:
            current_user.name = sanitize_text(data.name) or data.name
        if data.major is not None:
            current_user.major = sanitize_text(data.major) or data.major
        if data.school is not None:
            current_user.school = sanitize_text(data.school) or data.school
        if data.city is not None:
            current_user.city = sanitize_text(data.city) or data.city
        if data.district is not None:
            current_user.district = sanitize_text(data.district)
        if data.address_detail is not None:
            current_user.address_detail = sanitize_text(data.address_detail)
        if data.avatar_id is not None:
            current_user.avatar_id = data.avatar_id
        if data.bio is not None:
            current_user.bio = sanitize_text(data.bio)

        # Cập nhật danh sách môn học nếu được cung cấp
        if data.subjects is not None:
            # Xóa các môn học cũ
            await db.execute(
                delete(UserSubject).where(UserSubject.user_id == current_user.id)
            )
            # Thêm danh sách môn học mới
            for subj in set(data.subjects):
                clean_subj = sanitize_text(subj)
                if clean_subj:
                    new_subj = UserSubject(user_id=current_user.id, subject_name=clean_subj)
                    db.add(new_subj)

        await db.commit()
        await db.refresh(current_user)

        # Invalidate feed cache của user này khi thông tin trường/môn thay đổi
        from app.utils.memory_cache import cache
        cache.invalidate_prefix(f"feed:{current_user.id}")

        return await UserService.get_profile(db, current_user.id)


user_service = UserService()
