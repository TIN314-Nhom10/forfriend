import math
import uuid
from typing import List
import bleach
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.rating import Rating
from app.models.room import Room, RoomParticipant
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingResponse, UserRatingsResponse
from app.schemas.room import UserBrief
from app.utils.memory_cache import memory_cache


class RatingService:
    """Service xử lý đánh giá bạn học (Hero Rating) và điểm uy tín."""

    async def create_rating(
        self,
        db: AsyncSession,
        rater: User,
        data: RatingCreate,
    ) -> RatingResponse:
        """Đánh giá bạn học (1-5 sao) sau khi tham gia phòng học."""
        # 1. Không thể tự đánh giá chính mình
        if rater.id == data.ratee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn không thể tự đánh giá chính mình",
            )

        # 2. Kiểm tra phòng học tồn tại
        room = await db.get(Room, data.room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        # 3. Kiểm tra người được đánh giá tồn tại
        ratee = await db.get(User, data.ratee_id)
        if not ratee or not ratee.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Người được đánh giá không tồn tại hoặc đã bị vô hiệu hóa",
            )

        # 4. Kiểm tra cả rater và ratee đều từng ở cùng phòng này (accepted hoặc left)
        rater_in_room = (room.host_id == rater.id)
        if not rater_in_room:
            rp_stmt = select(RoomParticipant).where(
                RoomParticipant.room_id == data.room_id,
                RoomParticipant.user_id == rater.id,
                RoomParticipant.status.in_(["accepted", "left"]),
            )
            rater_in_room = (await db.execute(rp_stmt)).scalar_one_or_none() is not None

        if not rater_in_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bạn chưa từng tham gia phòng học này",
            )

        ratee_in_room = (room.host_id == ratee.id)
        if not ratee_in_room:
            ep_stmt = select(RoomParticipant).where(
                RoomParticipant.room_id == data.room_id,
                RoomParticipant.user_id == ratee.id,
                RoomParticipant.status.in_(["accepted", "left"]),
            )
            ratee_in_room = (await db.execute(ep_stmt)).scalar_one_or_none() is not None

        if not ratee_in_room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Người được đánh giá không tham gia cùng phòng học này với bạn",
            )

        # 5. Kiểm tra duplicate rating trong cùng 1 phòng
        dup_stmt = select(Rating).where(
            Rating.rater_id == rater.id,
            Rating.ratee_id == data.ratee_id,
            Rating.room_id == data.room_id,
        )
        existing_rating = (await db.execute(dup_stmt)).scalar_one_or_none()
        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bạn đã đánh giá bạn học này trong phòng học này rồi",
            )

        # 6. Tạo Rating record
        clean_comment = bleach.clean(data.comment.strip()) if data.comment else None
        rating = Rating(
            rater_id=rater.id,
            ratee_id=data.ratee_id,
            room_id=data.room_id,
            stars=data.stars,
            comment=clean_comment,
        )
        db.add(rating)

        # 7. Cập nhật avg_rating và total_ratings của ratee
        old_total = ratee.total_ratings
        old_avg = ratee.avg_rating
        new_total = old_total + 1
        new_avg = round(((old_avg * old_total) + data.stars) / new_total, 2)
        ratee.total_ratings = new_total
        ratee.avg_rating = new_avg

        # Xóa cache feed để matching algorithm cập nhật author rating mới
        memory_cache.invalidate_prefix("feed:")

        await db.commit()
        await db.refresh(rating)

        return RatingResponse(
            id=rating.id,
            rater=UserBrief.model_validate(rater),
            ratee=UserBrief.model_validate(ratee),
            room_id=rating.room_id,
            stars=rating.stars,
            comment=rating.comment,
            created_at=rating.created_at,
        )

    async def get_user_ratings(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        page: int = 1,
        per_page: int = 20,
    ) -> UserRatingsResponse:
        """Lấy danh sách đánh giá nhận được của một Hero, sắp xếp mới nhất, có phân trang."""
        user = await db.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Người dùng không tồn tại",
            )

        query = (
            select(Rating)
            .options(joinedload(Rating.rater), joinedload(Rating.ratee))
            .where(Rating.ratee_id == user_id)
            .order_by(Rating.created_at.desc())
        )

        count_stmt = select(func.count(Rating.id)).where(Rating.ratee_id == user_id)
        total = (await db.execute(count_stmt)).scalar_one()

        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        ratings = (await db.execute(query)).scalars().all()

        items = [
            RatingResponse(
                id=r.id,
                rater=UserBrief.model_validate(r.rater),
                ratee=UserBrief.model_validate(r.ratee),
                room_id=r.room_id,
                stars=r.stars,
                comment=r.comment,
                created_at=r.created_at,
            )
            for r in ratings
        ]
        total_pages = max(1, math.ceil(total / per_page)) if total > 0 else 1

        return UserRatingsResponse(
            items=items,
            total=total,
            avg_rating=user.avg_rating,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    async def get_pending_ratings(
        self,
        db: AsyncSession,
        user: User,
        room_id: uuid.UUID,
    ) -> List[UserBrief]:
        """Lấy danh sách các bạn học trong phòng mà user chưa đánh giá."""
        room = await db.get(Room, room_id)
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Phòng học không tồn tại",
            )

        # Gom tất cả ứng viên trong phòng (Host + các thành viên accepted/left) ngoại trừ user
        candidate_ids = set()
        if room.host_id != user.id:
            candidate_ids.add(room.host_id)

        part_stmt = select(RoomParticipant.user_id).where(
            RoomParticipant.room_id == room_id,
            RoomParticipant.status.in_(["accepted", "left"]),
            RoomParticipant.user_id != user.id,
        )
        part_user_ids = (await db.execute(part_stmt)).scalars().all()
        candidate_ids.update(part_user_ids)

        if not candidate_ids:
            return []

        # Lấy danh sách những người user đã đánh giá trong phòng này
        rated_stmt = select(Rating.ratee_id).where(
            Rating.rater_id == user.id,
            Rating.room_id == room_id,
        )
        rated_ids = set((await db.execute(rated_stmt)).scalars().all())

        pending_ids = list(candidate_ids - rated_ids)
        if not pending_ids:
            return []

        users_stmt = select(User).where(User.id.in_(pending_ids))
        users = (await db.execute(users_stmt)).scalars().all()

        return [UserBrief.model_validate(u) for u in users]


rating_service = RatingService()
