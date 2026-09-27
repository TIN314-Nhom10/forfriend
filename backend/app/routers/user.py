import uuid
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.rating import UserRatingsResponse
from app.schemas.user import FileUploadResponse, UserProfile, UserPublic, UserUpdate
from app.services.upload_service import upload_service
from app.services.user_service import user_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserProfile,
    summary="Xem thông tin hồ sơ Hero của chính mình",
)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy toàn bộ thông tin hồ sơ cá nhân của người dùng đang đăng nhập."""
    return await user_service.get_profile(db, current_user.id)


@router.put(
    "/me",
    response_model=UserProfile,
    summary="Cập nhật thông tin hồ sơ Hero",
)
async def update_my_profile(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Cập nhật từng phần thông tin Hero:
    - Họ tên, trường, ngành, thành phố, địa chỉ, tiểu sử
    - Đổi avatar chibi (1 đến 15)
    - Cập nhật danh sách môn học quan tâm
    """
    return await user_service.update_profile(db, current_user, data)


@router.put(
    "/me/avatar",
    response_model=UserProfile,
    summary="Đổi avatar chibi",
)
async def update_my_avatar(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cập nhật avatar chibi từ 1 đến 15."""
    avatar_id = int(data.get("avatar_id", 1))
    return await user_service.update_profile(db, current_user, UserUpdate(avatar_id=avatar_id))


@router.post(
    "/me/upload-student-id",
    response_model=FileUploadResponse,
    summary="Upload thẻ sinh viên & xác thực Gemini",
)
async def upload_student_id_me(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tải lên ảnh thẻ SV và gắn vào tài khoản sau khi xác thực AI."""
    from app.services.ai_verification_service import ai_verification_service

    content = await file.read()
    await file.seek(0)

    ai_result = await ai_verification_service.verify_student_id(
        image_bytes=content,
        mime_type=file.content_type or "image/jpeg",
        expected_name=current_user.name,
        expected_school=current_user.school,
    )

    url = await upload_service.upload_student_id(file)
    current_user.student_id_card_url = url
    await db.commit()
    return FileUploadResponse(
        url=url,
        message=ai_result.get("message", "Verified"),
        verification=ai_result,
    )


@router.post(
    "/me/upload-cv",
    response_model=FileUploadResponse,
    summary="Upload file CV PDF",
)
async def upload_cv_me(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tải lên file CV PDF và gắn vào tài khoản."""
    url = await upload_service.upload_cv(file)
    current_user.cv_url = url
    await db.commit()
    return FileUploadResponse(url=url)


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="Xem thông tin hồ sơ công khai của bạn học khác",
)
async def get_user_public_profile(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Xem hồ sơ công khai (tên, trường, ngành, avatar, rating, môn học) của bạn học bất kỳ."""
    return await user_service.get_public_profile(db, user_id)


@router.get(
    "/{user_id}/ratings",
    response_model=UserRatingsResponse,
    summary="Xem danh sách đánh giá nhận được của một Hero",
)
async def get_user_ratings_list(
    user_id: uuid.UUID,
    page: int = Query(default=1, ge=1, description="Số trang"),
    per_page: int = Query(default=20, ge=1, le=50, description="Số đánh giá mỗi trang"),
    db: AsyncSession = Depends(get_db),
):
    """Xem danh sách các đánh giá nhận được của một Hero kèm điểm trung bình."""
    from app.services.rating_service import rating_service
    return await rating_service.get_user_ratings(db, user_id, page, per_page)
