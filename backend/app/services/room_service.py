import math
import uuid
from datetime import datetime, timezone
from typing import List, Optional
import bleach
from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.config import settings
from app.models.room import Room, RoomCategory, RoomParticipant
from app.models.user import User
from app.schemas.room import (
    ApproveResponse,
    JoinRequestResponse,
    ParticipantResponse,
    RoomCategoryResponse,
    RoomCreate,
    RoomDetailResponse,
    RoomListResponse,
    RoomResponse,
    RoomTokenResponse,
    UserBrief,
)
from app.services.livekit_service import livekit_service
from app.utils.room_code import get_unique_room_code
from app.websockets.connection_manager import notification_manager


class RoomService:
    """Service xử lý nghiệp vụ Phòng học ảo (Adventure Zones) & In-Memory Real-time Hub."""

    async def create_room(self, db: AsyncSession, host: User, data: RoomCreate) -> RoomResponse:
        """Tạo phòng học mới và tự động thêm Host làm participant đầu tiên (status=accepted)."""
        # 1. Validate Category tồn tại
        category = await db.get(RoomCategory, data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Danh mục phân khu (category) không tồn tại",
            )

        # 2. Sinh room_code 6 ký tự duy nhất
        room_code = await get_unique_room_code(db)

        # 3. Tạo record Room
        room = Room(
            host_id=host.id,
            name=bleach.clean(data.name.strip()),
            topic=bleach.clean(data.topic.strip()),
            category_id=data.category_id,
            room_code=room_code,
            status="waiting",
            max_participants=data.max_participants,
            current_participants=1,
        )
        db.add(room)
        await db.flush()

        # 4. Tạo participant cho Host
        host_participant = RoomParticipant(
            room_id=room.id,
            user_id=host.id,
            status="accepted",
            joined_at=datetime.now(timezone.utc),
        )
        db.add(host_participant)
        await db.commit()

        # Nạp relationships để trả về Response
        result = await db.execute(
            select(Room)
            .options(joinedload(Room.host), joinedload(Room.category))
            .where(Room.id == room.id)
        )
        saved_room = result.scalar_one()

        return RoomResponse.model_validate(saved_room)

    async def get_rooms(
        self,
        db: AsyncSession,
        page: int = 1,
        per_page: int = 20,
        category_id: Optional[uuid.UUID] = None,
        status_filter: Optional[str] = None,
        search: Optional[str] = None,
        current_user: Optional[User] = None,
    ) -> RoomListResponse:
        """Lấy danh sách phòng học ở sảnh chờ (Lobby), hỗ trợ lọc theo category, status và tìm kiếm."""
        query = select(Room).options(
            joinedload(Room.host),
            joinedload(Room.category),
        )

        # Lọc theo status (mặc định waiting,active)
        if status_filter:
            statuses = [s.strip() for s in status_filter.split(",") if s.strip()]
            if statuses:
                query = query.where(Room.status.in_(statuses))
        else:
            query = query.where(Room.status.in_(["waiting", "active"]))

        # Lọc theo category
        if category_id:
            query = query.where(Room.category_id == category_id)

        # Tìm kiếm theo tên hoặc chủ đề
        if search and search.strip():
            s = f"%{search.strip().lower()}%"
            query = query.where(
                or_(
                    func.lower(Room.name).ilike(s),
                    func.lower(Room.topic).ilike(s),
                )
            )

        # Đếm tổng số lượng records phù hợp
        count_stmt = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_stmt)).scalar_one()

        # Sắp xếp mới nhất
        query = query.order_by(Room.created_at.desc())

        # Phân trang
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        result = await db.execute(query)
        rooms = list(result.scalars().all())

        items = [RoomResponse.model_validate(r) for r in rooms]
        total_pages = max(1, math.ceil(total / per_page)) if total > 0 else 1

        return RoomListResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    async def get_categories(self, db: AsyncSession) -> List[RoomCategoryResponse]:
        """Lấy danh sách phân khu danh mục kèm số lượng phòng đang active/waiting."""
        categories_result = await db.execute(
            select(RoomCategory).order_by(RoomCategory.display_order.asc())
        )
        categories = list(categories_result.scalars().all())

        # Thống kê số phòng active theo category
        count_stmt = (
            select(Room.category_id, func.count(Room.id))
            .where(Room.status.in_(["waiting", "active"]))
            .group_by(Room.category_id)
        )
        count_result = await db.execute(count_stmt)
        count_map = dict(count_result.all())

        responses = []
        for cat in categories:
            cat_resp = RoomCategoryResponse(
                id=cat.id,
                name=cat.name,
                icon=cat.icon,
                color=cat.color,
                display_order=cat.display_order,
                active_rooms_count=count_map.get(cat.id, 0),
            )
            responses.append(cat_resp)

        return responses

    async def get_room_detail(self, db: AsyncSession, room_id: uuid.UUID) -> RoomDetailResponse:
        """Lấy chi tiết phòng học kèm danh sách thành viên tham gia."""
        result = await db.execute(
            select(Room)
            .options(
                joinedload(Room.host),
                joinedload(Room.category),
                selectinload(Room.participants).joinedload(RoomParticipant.user),
            )
            .where(Room.id == room_id)
        )
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        participants = [
            ParticipantResponse(
                id=p.id,
                room_id=p.room_id,
                user=UserBrief.model_validate(p.user),
                status=p.status,
                requested_at=p.requested_at,
                joined_at=p.joined_at,
                left_at=p.left_at,
            )
            for p in room.participants
        ]

        return RoomDetailResponse(
            id=room.id,
            name=room.name,
            room_code=room.room_code,
            topic=room.topic,
            category=RoomCategoryResponse.model_validate(room.category) if room.category else None,
            host=UserBrief.model_validate(room.host),
            status=room.status,
            max_participants=room.max_participants,
            current_participants=room.current_participants,
            created_at=room.created_at,
            closed_at=room.closed_at,
            participants=participants,
        )

    async def request_join(
        self,
        db: AsyncSession,
        room_id: uuid.UUID,
        user: User,
    ) -> JoinRequestResponse:
        """Khách gửi yêu cầu xin vào phòng và gửi thông báo real-time tới Host."""
        result = await db.execute(
            select(Room).options(joinedload(Room.host)).where(Room.id == room_id)
        )
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        if room.status == "closed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phòng học đã đóng",
            )

        if room.host_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn là Host của phòng học này",
            )

        if room.current_participants >= room.max_participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phòng học đã đầy",
            )

        # Kiểm tra trạng thái tham gia trước đó
        p_stmt = select(RoomParticipant).where(
            RoomParticipant.room_id == room_id,
            RoomParticipant.user_id == user.id,
        )
        existing_p = (await db.execute(p_stmt)).scalar_one_or_none()

        now = datetime.now(timezone.utc)
        if existing_p:
            if existing_p.status == "accepted":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Bạn đã là thành viên trong phòng này",
                )
            if existing_p.status == "pending":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Yêu cầu tham gia của bạn đang chờ Host phê duyệt",
                )
            # Nếu đã từng bị reject hoặc đã left, cho phép xin lại
            existing_p.status = "pending"
            existing_p.requested_at = now
            participant = existing_p
        else:
            participant = RoomParticipant(
                room_id=room.id,
                user_id=user.id,
                status="pending",
                requested_at=now,
            )
            db.add(participant)

        await db.commit()
        await db.refresh(participant)

        # Bắn WebSocket notification tới Host trong RAM
        await notification_manager.send_to_user(
            str(room.host_id),
            {
                "type": "room_request",
                "data": {
                    "room_id": str(room.id),
                    "room_name": room.name,
                    "user": {
                        "id": str(user.id),
                        "name": user.name,
                        "avatar_id": user.avatar_id,
                        "school": user.school,
                        "avg_rating": user.avg_rating,
                    },
                },
            },
        )

        return JoinRequestResponse(
            participant_id=participant.id,
            status="pending",
            message="Yêu cầu đã được gửi tới host",
        )

    async def approve_request(
        self,
        db: AsyncSession,
        room_id: uuid.UUID,
        host: User,
        target_user_id: uuid.UUID,
    ) -> ApproveResponse:
        """Host phê duyệt yêu cầu tham gia của khách."""
        room = await db.get(Room, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        if room.host_id != host.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ Host mới có quyền phê duyệt thành viên",
            )

        if room.status == "closed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phòng học đã đóng",
            )

        if room.current_participants >= room.max_participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phòng học đã đạt giới hạn số lượng thành viên",
            )

        p_stmt = select(RoomParticipant).where(
            RoomParticipant.room_id == room_id,
            RoomParticipant.user_id == target_user_id,
        )
        participant = (await db.execute(p_stmt)).scalar_one_or_none()
        if not participant or participant.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không tìm thấy yêu cầu tham gia hợp lệ",
            )

        now = datetime.now(timezone.utc)
        participant.status = "accepted"
        participant.joined_at = now
        room.current_participants += 1

        if room.status == "waiting":
            room.status = "active"

        await db.commit()

        # Tạo LiveKit access token cho thành viên được duyệt
        target_user = await db.get(User, target_user_id)
        livekit_token = livekit_service.generate_token(
            room_name=room.room_code,
            participant_identity=str(target_user_id),
            participant_name=target_user.name if target_user else "Hero Member",
            avatar_id=target_user.avatar_id if target_user else 1,
            is_host=False,
        )

        # Bắn WebSocket notification tới khách được duyệt
        await notification_manager.send_to_user(
            str(target_user_id),
            {
                "type": "room_approved",
                "data": {
                    "room_id": str(room.id),
                    "room_name": room.name,
                    "livekit_token": livekit_token,
                    "livekit_url": settings.LIVEKIT_URL,
                },
            },
        )

        return ApproveResponse(
            status="accepted",
            livekit_token=livekit_token,
            livekit_url=settings.LIVEKIT_URL,
        )

    async def reject_request(
        self,
        db: AsyncSession,
        room_id: uuid.UUID,
        host: User,
        target_user_id: uuid.UUID,
    ) -> dict:
        """Host từ chối yêu cầu tham gia của khách."""
        room = await db.get(Room, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        if room.host_id != host.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ Host mới có quyền từ chối yêu cầu",
            )

        p_stmt = select(RoomParticipant).where(
            RoomParticipant.room_id == room_id,
            RoomParticipant.user_id == target_user_id,
        )
        participant = (await db.execute(p_stmt)).scalar_one_or_none()
        if not participant or participant.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không tìm thấy yêu cầu tham gia hợp lệ",
            )

        participant.status = "rejected"
        await db.commit()

        # Bắn WebSocket notification tới khách bị từ chối
        await notification_manager.send_to_user(
            str(target_user_id),
            {
                "type": "room_rejected",
                "data": {"room_id": str(room.id)},
            },
        )

        return {"status": "rejected", "message": "Đã từ chối yêu cầu tham gia"}

    async def leave_room(
        self,
        db: AsyncSession,
        room_id: uuid.UUID,
        user: User,
    ) -> dict:
        """Thành viên rời phòng; nếu Host rời phòng thì tự động kết thúc phòng học."""
        result = await db.execute(
            select(Room)
            .options(selectinload(Room.participants))
            .where(Room.id == room_id)
        )
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        p_stmt = select(RoomParticipant).where(
            RoomParticipant.room_id == room_id,
            RoomParticipant.user_id == user.id,
        )
        participant = (await db.execute(p_stmt)).scalar_one_or_none()
        if not participant or participant.status != "accepted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn không phải là thành viên đang hoạt động trong phòng",
            )

        now = datetime.now(timezone.utc)

        # Trường hợp Host rời phòng -> Đóng phòng luôn
        if room.host_id == user.id:
            room.status = "closed"
            room.closed_at = now
            participant.status = "left"
            participant.left_at = now
            await db.commit()

            # Thông báo cho tất cả thành viên khác
            other_uids = [
                str(p.user_id)
                for p in room.participants
                if p.status == "accepted" and p.user_id != user.id
            ]
            if other_uids:
                await notification_manager.broadcast_to_users(
                    other_uids,
                    {"type": "room_closed", "data": {"room_id": str(room.id)}},
                )

            # Đóng phòng trên LiveKit Cloud
            await livekit_service.close_room(room.room_code)

            return {
                "status": "closed",
                "message": "Host đã rời phòng, phòng học đã kết thúc",
            }

        # Trường hợp thành viên thông thường rời phòng
        participant.status = "left"
        participant.left_at = now
        room.current_participants = max(1, room.current_participants - 1)
        await db.commit()

        return {"status": "left", "message": "Đã rời phòng thành công"}

    async def close_room(
        self,
        db: AsyncSession,
        room_id: uuid.UUID,
        host: User,
    ) -> dict:
        """Host chủ động đóng phòng học và ngắt kết nối các thành viên."""
        result = await db.execute(
            select(Room)
            .options(selectinload(Room.participants))
            .where(Room.id == room_id)
        )
        room = result.scalar_one_or_none()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        if room.host_id != host.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Chỉ Host mới có quyền đóng phòng học",
            )

        now = datetime.now(timezone.utc)
        room.status = "closed"
        room.closed_at = now
        await db.commit()

        # Thông báo tới tất cả thành viên khác trong phòng
        other_uids = [
            str(p.user_id)
            for p in room.participants
            if p.status == "accepted" and p.user_id != host.id
        ]
        if other_uids:
            await notification_manager.broadcast_to_users(
                other_uids,
                {"type": "room_closed", "data": {"room_id": str(room.id)}},
            )

        # Đóng phòng trên LiveKit Cloud
        await livekit_service.close_room(room.room_code)

        return {"status": "closed", "message": "Đã đóng phòng thành công"}

    async def get_room_token(
        self,
        db: AsyncSession,
        room_id: uuid.UUID,
        user: User,
    ) -> RoomTokenResponse:
        """Lấy token LiveKit WebRTC cho Host hoặc thành viên đã được duyệt."""
        room = await db.get(Room, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        if room.status == "closed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phòng học đã đóng",
            )

        is_host = (room.host_id == user.id)
        if not is_host:
            p_stmt = select(RoomParticipant).where(
                RoomParticipant.room_id == room_id,
                RoomParticipant.user_id == user.id,
                RoomParticipant.status == "accepted",
            )
            p = (await db.execute(p_stmt)).scalar_one_or_none()
            if not p:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Bạn chưa được chấp nhận vào phòng học này",
                )

        token = livekit_service.generate_token(
            room_name=room.room_code,
            participant_identity=str(user.id),
            participant_name=user.name,
            avatar_id=user.avatar_id,
            is_host=is_host,
        )

        return RoomTokenResponse(
            room_id=room.id,
            room_code=room.room_code,
            livekit_token=token,
            livekit_url=settings.LIVEKIT_URL,
            token=token,
            url=settings.LIVEKIT_URL,
            is_host=is_host,
        )


room_service = RoomService()
