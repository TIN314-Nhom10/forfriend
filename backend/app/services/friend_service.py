import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.friendship import Friendship
from app.models.user import User
from app.schemas.friend_chat import (
    FriendActionResponse,
    FriendRequestResponse,
    FriendResponse,
)
from app.schemas.room import UserBrief
from app.websockets.connection_manager import connection_manager, notification_manager


class FriendService:
    """Service xử lý hệ thống kết bạn (Hero Friends) và danh sách bạn bè."""

    async def send_request(
        self,
        db: AsyncSession,
        requester: User,
        addressee_id: uuid.UUID,
    ) -> FriendRequestResponse:
        """Gửi lời mời kết bạn tới một Hero khác."""
        # 1. Không tự kết bạn với chính mình
        if requester.id == addressee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể tự kết bạn với chính mình",
            )

        # 2. Kiểm tra user nhận lời mời tồn tại
        addressee = await db.get(User, addressee_id)
        if not addressee or not addressee.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Người dùng không tồn tại hoặc đã bị vô hiệu hóa",
            )

        # 3. Kiểm tra mối quan hệ 2 chiều đã có chưa
        stmt = select(Friendship).where(
            or_(
                and_(Friendship.requester_id == requester.id, Friendship.addressee_id == addressee_id),
                and_(Friendship.requester_id == addressee_id, Friendship.addressee_id == requester.id),
            )
        )
        existing = (await db.execute(stmt)).scalar_one_or_none()

        now = datetime.now(timezone.utc)
        if existing:
            if existing.status == "accepted":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Hai bạn đã là bạn bè của nhau rồi",
                )
            if existing.status == "pending":
                if existing.requester_id == requester.id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Bạn đã gửi lời mời kết bạn trước đó rồi",
                    )
                else:
                    # Người kia đã gửi lời mời trước đó -> Tự động thành bạn bè luôn!
                    existing.status = "accepted"
                    existing.responded_at = now
                    await db.commit()

                    # Thông báo friend_accepted tới cả người kia
                    await notification_manager.send_to_user(
                        str(addressee_id),
                        {
                            "type": "friend_accepted",
                            "data": {
                                "friendship_id": str(existing.id),
                                "friend": {
                                    "id": str(requester.id),
                                    "name": requester.name,
                                    "avatar_id": requester.avatar_id,
                                    "school": requester.school,
                                    "avg_rating": requester.avg_rating,
                                },
                            },
                        },
                    )
                    return FriendRequestResponse(
                        friendship_id=existing.id,
                        from_user=UserBrief.model_validate(requester),
                        created_at=existing.created_at,
                    )
            # Nếu từng bị rejected hoặc blocked, cho phép gửi lại
            existing.requester_id = requester.id
            existing.addressee_id = addressee_id
            existing.status = "pending"
            existing.created_at = now
            existing.responded_at = None
            friendship = existing
        else:
            friendship = Friendship(
                requester_id=requester.id,
                addressee_id=addressee_id,
                status="pending",
                created_at=now,
            )
            db.add(friendship)

        await db.commit()
        await db.refresh(friendship)

        # Bắn WebSocket notification tới addressee
        await notification_manager.send_to_user(
            str(addressee_id),
            {
                "type": "friend_request",
                "data": {
                    "friendship_id": str(friendship.id),
                    "from": {
                        "id": str(requester.id),
                        "name": requester.name,
                        "avatar_id": requester.avatar_id,
                        "school": requester.school,
                        "avg_rating": requester.avg_rating,
                    },
                },
            },
        )

        return FriendRequestResponse(
            friendship_id=friendship.id,
            from_user=UserBrief.model_validate(requester),
            created_at=friendship.created_at,
        )

    async def accept_request(
        self,
        db: AsyncSession,
        friendship_id: uuid.UUID,
        user: User,
    ) -> FriendActionResponse:
        """Chấp nhận lời mời kết bạn."""
        friendship = await db.get(Friendship, friendship_id)
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy lời mời kết bạn",
            )

        if friendship.addressee_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền chấp nhận lời mời này",
            )

        if friendship.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lời mời kết bạn không ở trạng thái chờ duyệt",
            )

        now = datetime.now(timezone.utc)
        friendship.status = "accepted"
        friendship.responded_at = now
        await db.commit()

        # Bắn WebSocket event friend_accepted tới requester
        await notification_manager.send_to_user(
            str(friendship.requester_id),
            {
                "type": "friend_accepted",
                "data": {
                    "friendship_id": str(friendship.id),
                    "friend": {
                        "id": str(user.id),
                        "name": user.name,
                        "avatar_id": user.avatar_id,
                        "school": user.school,
                        "avg_rating": user.avg_rating,
                    },
                },
            },
        )

        return FriendActionResponse(message="Đã chấp nhận lời mời kết bạn", status="accepted")

    async def reject_request(
        self,
        db: AsyncSession,
        friendship_id: uuid.UUID,
        user: User,
    ) -> FriendActionResponse:
        """Từ chối lời mời kết bạn."""
        friendship = await db.get(Friendship, friendship_id)
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy lời mời kết bạn",
            )

        if friendship.addressee_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền từ chối lời mời này",
            )

        now = datetime.now(timezone.utc)
        friendship.status = "rejected"
        friendship.responded_at = now
        await db.commit()

        return FriendActionResponse(message="Đã từ chối lời mời kết bạn", status="rejected")

    async def remove_friend(
        self,
        db: AsyncSession,
        user: User,
        friend_id: uuid.UUID,
    ) -> FriendActionResponse:
        """Hủy kết bạn với một người bạn."""
        stmt = select(Friendship).where(
            or_(
                and_(Friendship.requester_id == user.id, Friendship.addressee_id == friend_id),
                and_(Friendship.requester_id == friend_id, Friendship.addressee_id == user.id),
            ),
            Friendship.status == "accepted",
        )
        friendship = (await db.execute(stmt)).scalar_one_or_none()
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy mối quan hệ bạn bè",
            )

        await db.delete(friendship)
        await db.commit()

        return FriendActionResponse(message="Đã hủy kết bạn thành công", status="removed")

    async def get_friends(self, db: AsyncSession, user: User) -> List[FriendResponse]:
        """Lấy danh sách bạn bè đã chấp nhận kèm trạng thái Online/Offline."""
        stmt = (
            select(Friendship)
            .options(joinedload(Friendship.requester), joinedload(Friendship.addressee))
            .where(
                Friendship.status == "accepted",
                or_(Friendship.requester_id == user.id, Friendship.addressee_id == user.id),
            )
            .order_by(Friendship.responded_at.desc(), Friendship.created_at.desc())
        )
        friendships = (await db.execute(stmt)).scalars().all()

        items = []
        for f in friendships:
            friend_user = f.addressee if f.requester_id == user.id else f.requester
            is_online = connection_manager.is_user_online(str(friend_user.id))
            since = f.responded_at or f.created_at
            items.append(
                FriendResponse(
                    friendship_id=f.id,
                    friend=UserBrief.model_validate(friend_user),
                    is_online=is_online,
                    since=since,
                )
            )

        return items

    async def get_friend_requests(self, db: AsyncSession, user: User) -> List[FriendRequestResponse]:
        """Lấy danh sách lời mời kết bạn đang chờ duyệt gửi tới user."""
        stmt = (
            select(Friendship)
            .options(joinedload(Friendship.requester))
            .where(
                Friendship.addressee_id == user.id,
                Friendship.status == "pending",
            )
            .order_by(Friendship.created_at.desc())
        )
        friendships = (await db.execute(stmt)).scalars().all()

        return [
            FriendRequestResponse(
                friendship_id=f.id,
                from_user=UserBrief.model_validate(f.requester),
                created_at=f.created_at,
            )
            for f in friendships
        ]

    async def are_friends(self, db: AsyncSession, user_id_1: uuid.UUID, user_id_2: uuid.UUID) -> bool:
        """Kiểm tra hai người dùng có phải là bạn bè đã chấp nhận không."""
        stmt = select(Friendship.id).where(
            Friendship.status == "accepted",
            or_(
                and_(Friendship.requester_id == user_id_1, Friendship.addressee_id == user_id_2),
                and_(Friendship.requester_id == user_id_2, Friendship.addressee_id == user_id_1),
            ),
        )
        return (await db.execute(stmt)).scalar_one_or_none() is not None


friend_service = FriendService()
