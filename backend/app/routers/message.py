import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.friend_chat import (
    ConversationResponse,
    MessageCreateRequest,
    MessageListResponse,
    MessageResponse,
)
from app.services.message_service import message_service
from app.utils.dependencies import get_current_user
from fastapi import status

router = APIRouter(prefix="/api/v1/messages", tags=["Messages"])


@router.post("/{friend_id}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message_rest(
    friend_id: uuid.UUID,
    data: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gửi tin nhắn 1-1 qua REST API."""
    return await message_service.create_message(
        db=db,
        sender_id=current_user.id,
        receiver_id=friend_id,
        content=data.content,
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách tất cả các cuộc trò chuyện của user, sắp xếp theo tin nhắn mới nhất."""
    return await message_service.get_conversations(db, current_user)


@router.get("/{friend_id}", response_model=MessageListResponse)
async def get_messages(
    friend_id: uuid.UUID,
    before: Optional[datetime] = Query(default=None, description="Cursor timestamp để lấy tin nhắn cũ hơn"),
    limit: int = Query(default=50, ge=1, le=100, description="Số lượng tin nhắn tối đa"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy lịch sử tin nhắn 1-1 giữa user và một người bạn."""
    return await message_service.get_messages(db, current_user, friend_id, before, limit)


@router.post("/{friend_id}/read")
async def mark_messages_as_read(
    friend_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Đánh dấu tất cả tin nhắn từ bạn bè gửi tới là đã đọc."""
    count = await message_service.mark_read(db, current_user.id, friend_id)
    return {"marked_count": count, "status": "read"}
