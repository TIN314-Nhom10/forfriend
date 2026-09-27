import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.friend_chat import (
    FriendActionResponse,
    FriendRequestResponse,
    FriendResponse,
)
from app.services.friend_service import friend_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/friends", tags=["Friends"])


@router.post("/request/{user_id}", response_model=FriendRequestResponse, status_code=status.HTTP_201_CREATED)
async def send_friend_request(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gửi lời mời kết bạn tới một Hero khác."""
    return await friend_service.send_request(db, current_user, user_id)


@router.post("/accept/{friendship_id}", response_model=FriendActionResponse)
async def accept_friend_request(
    friendship_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Chấp nhận lời mời kết bạn."""
    return await friend_service.accept_request(db, friendship_id, current_user)


@router.post("/reject/{friendship_id}", response_model=FriendActionResponse)
async def reject_friend_request(
    friendship_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Từ chối lời mời kết bạn."""
    return await friend_service.reject_request(db, friendship_id, current_user)


@router.get("/requests", response_model=List[FriendRequestResponse])
async def get_incoming_requests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Xem danh sách các lời mời kết bạn đang chờ duyệt."""
    return await friend_service.get_friend_requests(db, current_user)


@router.get("/", response_model=List[FriendResponse])
async def get_friends_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách bạn bè kèm trạng thái Online/Offline."""
    return await friend_service.get_friends(db, current_user)


@router.delete("/{user_id}", response_model=FriendActionResponse)
async def remove_friend(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Hủy kết bạn với một người bạn."""
    return await friend_service.remove_friend(db, current_user, user_id)
