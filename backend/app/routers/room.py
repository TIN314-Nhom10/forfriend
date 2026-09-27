import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.room import (
    ApproveResponse,
    JoinRequestResponse,
    RoomCategoryResponse,
    RoomCreate,
    RoomDetailResponse,
    RoomListResponse,
    RoomResponse,
    RoomTokenResponse,
)
from app.services.room_service import room_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Tạo phòng học mới (Host tạo phòng và tự động trở thành thành viên đầu tiên)."""
    return await room_service.create_room(db, current_user, data)


@router.get("/categories", response_model=List[RoomCategoryResponse])
async def get_categories(
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách các phân khu môn học kèm số lượng phòng học đang hoạt động."""
    return await room_service.get_categories(db)


@router.get("/", response_model=RoomListResponse)
async def get_rooms(
    page: int = Query(default=1, ge=1, description="Số trang"),
    per_page: int = Query(default=20, ge=1, le=50, description="Số phòng mỗi trang"),
    category_id: Optional[uuid.UUID] = Query(default=None, description="Lọc theo phân khu danh mục"),
    status: Optional[str] = Query(default=None, description="Lọc theo trạng thái (waiting, active, closed)"),
    search: Optional[str] = Query(default=None, description="Tìm kiếm theo tên phòng hoặc chủ đề"),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách các phòng học tại sảnh chờ (Lobby)."""
    return await room_service.get_rooms(
        db=db,
        page=page,
        per_page=per_page,
        category_id=category_id,
        status_filter=status,
        search=search,
    )


@router.get("/{room_id}", response_model=RoomDetailResponse)
async def get_room_detail(
    room_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Xem thông tin chi tiết của phòng học và danh sách thành viên."""
    return await room_service.get_room_detail(db, room_id)


@router.get("/{room_id}/token", response_model=RoomTokenResponse)
async def get_room_token(
    room_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy token LiveKit WebRTC để kết nối video call (chỉ dành cho Host hoặc thành viên được duyệt)."""
    return await room_service.get_room_token(db, room_id, current_user)


@router.post("/{room_id}/request", response_model=JoinRequestResponse, status_code=status.HTTP_201_CREATED)
async def request_join_room(
    room_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gửi yêu cầu xin tham gia phòng học (bắn notification real-time tới Host)."""
    return await room_service.request_join(db, room_id, current_user)


@router.post("/{room_id}/approve/{user_id}", response_model=ApproveResponse)
async def approve_join_request(
    room_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Host phê duyệt yêu cầu tham gia của một thành viên."""
    return await room_service.approve_request(db, room_id, current_user, user_id)


@router.post("/{room_id}/reject/{user_id}")
async def reject_join_request(
    room_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Host từ chối yêu cầu tham gia của một thành viên."""
    return await room_service.reject_request(db, room_id, current_user, user_id)


@router.post("/{room_id}/leave")
async def leave_room(
    room_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Rời phòng học. Nếu Host rời phòng, toàn bộ phòng sẽ kết thúc."""
    return await room_service.leave_room(db, room_id, current_user)


@router.post("/{room_id}/close")
async def close_room(
    room_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Host chủ động đóng phòng học và thông báo giải tán phòng tới tất cả thành viên."""
    return await room_service.close_room(db, room_id, current_user)
