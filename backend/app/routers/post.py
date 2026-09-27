import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostListResponse,
    PostResponse,
    PostUpdate,
)
from app.services.post_service import post_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.post(
    "/",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo bài đăng tìm bạn học mới (Quest)",
)
async def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tạo bài đăng tìm bạn học nhóm:
    - Bắt buộc địa điểm (location) nếu chọn hình thức học offline
    - Tối đa 5 tags chủ đề môn học
    - Nội dung bài viết được làm sạch chống XSS
    """
    return await post_service.create_post(db, current_user, data)


@router.get(
    "/feed",
    response_model=PostListResponse,
    summary="Lấy danh sách bảng tin tìm bạn học (Feed)",
)
async def get_feed(
    page: int = Query(1, ge=1, description="Số thứ tự trang"),
    per_page: int = Query(20, ge=1, le=50, description="Số bài viết trên mỗi trang"),
    study_type: Optional[str] = Query(None, description="Lọc theo loại học: online hoặc offline"),
    tag: Optional[str] = Query(None, description="Lọc theo tag chủ đề môn học"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Lấy danh sách các bài đăng đang hoạt động:
    - Sắp xếp mới nhất theo thời gian tạo
    - Hỗ trợ lọc theo loại học (online/offline) và tag môn học
    - Hỗ trợ phân trang chuẩn
    """
    return await post_service.get_feed(
        db=db,
        user=current_user,
        page=page,
        per_page=per_page,
        study_type=study_type,
        tag=tag,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Xem chi tiết một bài đăng",
)
async def get_post(
    post_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy chi tiết một bài đăng theo ID."""
    return await post_service.get_post(db, post_id)


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    summary="Chỉnh sửa bài đăng (chỉ tác giả)",
)
async def update_post(
    post_id: uuid.UUID,
    data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Chỉnh sửa thông tin bài đăng. Chỉ người tạo bài viết mới có quyền này."""
    return await post_service.update_post(db, current_user.id, post_id, data)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa bài đăng (soft-delete, chỉ tác giả)",
)
async def delete_post(
    post_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Xóa bài đăng (đổi trạng thái is_active thành False). Chỉ người tạo bài mới có quyền xóa."""
    await post_service.delete_post(db, current_user.id, post_id)
