import uuid
from datetime import datetime, timezone
from typing import List, Optional
import bleach
from fastapi import HTTPException, status
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.models.user import User
from app.schemas.friend_chat import (
    ConversationResponse,
    MessageListResponse,
    MessageResponse,
)
from app.services.friend_service import friend_service


class MessageService:
    """Service xử lý tin nhắn 1-1 (Hero Direct Chat) và các cuộc trò chuyện."""

    async def create_message(
        self,
        db: AsyncSession,
        sender_id: uuid.UUID,
        receiver_id: uuid.UUID,
        content: str,
    ) -> Message:
        """Tạo tin nhắn mới sau khi xác thực 2 người đã là bạn bè."""
        # 1. Bắt buộc phải là bạn bè
        is_friend = await friend_service.are_friends(db, sender_id, receiver_id)
        if not is_friend:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn chỉ có thể gửi tin nhắn cho người đã là bạn bè",
            )

        # 2. Làm sạch nội dung tin nhắn chống XSS
        clean_content = bleach.clean(content.strip())
        if not clean_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nội dung tin nhắn không được để trống",
            )

        msg = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=clean_content,
        )
        db.add(msg)
        await db.commit()
        await db.refresh(msg)
        return msg

    async def get_messages(
        self,
        db: AsyncSession,
        user: User,
        friend_id: uuid.UUID,
        before: Optional[datetime] = None,
        limit: int = 50,
    ) -> MessageListResponse:
        """Lấy lịch sử tin nhắn giữa user và 1 người bạn (hỗ trợ cursor pagination theo timestamp)."""
        is_friend = await friend_service.are_friends(db, user.id, friend_id)
        if not is_friend:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn chỉ có thể xem tin nhắn với người đã là bạn bè",
            )

        query = select(Message).where(
            or_(
                and_(Message.sender_id == user.id, Message.receiver_id == friend_id),
                and_(Message.sender_id == friend_id, Message.receiver_id == user.id),
            )
        )
        if before:
            query = query.where(Message.created_at < before)

        query = query.order_by(Message.created_at.desc()).limit(limit + 1)
        messages = list((await db.execute(query)).scalars().all())

        has_more = len(messages) > limit
        items = messages[:limit]
        items.reverse()  # Sắp xếp xuôi thời gian

        response_items = [
            MessageResponse(
                id=m.id,
                sender_id=m.sender_id,
                receiver_id=m.receiver_id,
                content=m.content,
                is_mine=(m.sender_id == user.id),
                is_read=m.is_read,
                created_at=m.created_at,
                read_at=m.read_at,
            )
            for m in items
        ]

        return MessageListResponse(items=response_items, has_more=has_more)

    async def mark_read(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        friend_id: uuid.UUID,
    ) -> int:
        """Đánh dấu tất cả tin nhắn từ friend_id gửi tới user_id là đã đọc."""
        now = datetime.now(timezone.utc)
        stmt = (
            update(Message)
            .where(
                Message.sender_id == friend_id,
                Message.receiver_id == user_id,
                Message.is_read == False,
            )
            .values(is_read=True, read_at=now)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

    async def get_conversations(
        self,
        db: AsyncSession,
        user: User,
    ) -> List[ConversationResponse]:
        """Lấy danh sách tất cả các cuộc trò chuyện của user, sắp xếp theo tin nhắn mới nhất."""
        friends = await friend_service.get_friends(db, user)

        conversations = []
        for f in friends:
            friend_user_id = f.friend.id

            # Lấy tin nhắn mới nhất
            last_msg_stmt = (
                select(Message)
                .where(
                    or_(
                        and_(Message.sender_id == user.id, Message.receiver_id == friend_user_id),
                        and_(Message.sender_id == friend_user_id, Message.receiver_id == user.id),
                    )
                )
                .order_by(Message.created_at.desc())
                .limit(1)
            )
            last_msg = (await db.execute(last_msg_stmt)).scalar_one_or_none()

            # Đếm số tin chưa đọc từ bạn này
            unread_stmt = (
                select(func.count(Message.id))
                .where(
                    Message.sender_id == friend_user_id,
                    Message.receiver_id == user.id,
                    Message.is_read == False,
                )
            )
            unread_count = (await db.execute(unread_stmt)).scalar_one()

            last_msg_resp = (
                MessageResponse(
                    id=last_msg.id,
                    sender_id=last_msg.sender_id,
                    receiver_id=last_msg.receiver_id,
                    content=last_msg.content,
                    is_mine=(last_msg.sender_id == user.id),
                    is_read=last_msg.is_read,
                    created_at=last_msg.created_at,
                    read_at=last_msg.read_at,
                )
                if last_msg
                else None
            )

            conversations.append(
                ConversationResponse(
                    friend=f.friend,
                    is_online=f.is_online,
                    last_message=last_msg_resp,
                    unread_count=unread_count,
                )
            )

        # Sắp xếp: cuộc trò chuyện có tin nhắn mới nhất lên đầu
        conversations.sort(
            key=lambda c: (
                c.last_message.created_at if c.last_message else datetime.min.replace(tzinfo=timezone.utc)
            ),
            reverse=True,
        )

        return conversations


message_service = MessageService()
