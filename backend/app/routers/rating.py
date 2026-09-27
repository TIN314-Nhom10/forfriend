import uuid
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingResponse, UserRatingsResponse
from app.schemas.room import UserBrief
from app.services.rating_service import rating_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/ratings", tags=["Ratings"])


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(
    data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Gửi đánh giá (1-5 sao) cho bạn học sau khi tham gia phòng học."""
    return await rating_service.create_rating(db, current_user, data)


@router.get("/pending/{room_id}", response_model=List[UserBrief])
async def get_pending_ratings(
    room_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách các bạn học trong phòng mà người dùng hiện tại chưa đánh giá (phục vụ popup)."""
    return await rating_service.get_pending_ratings(db, current_user, room_id)


@router.get("/users/me", response_model=UserRatingsResponse)
@router.get("/me", response_model=UserRatingsResponse)
async def get_my_ratings(
    page: int = Query(default=1, ge=1, description="Số trang"),
    per_page: int = Query(default=20, ge=1, le=50, description="Số đánh giá mỗi trang"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy danh sách các đánh giá nhận được của chính mình."""
    return await rating_service.get_user_ratings(db, current_user.id, page, per_page)


@router.get("/user/{user_id}", response_model=UserRatingsResponse)
async def get_user_ratings(
    user_id: uuid.UUID,
    page: int = Query(default=1, ge=1, description="Số trang"),
    per_page: int = Query(default=20, ge=1, le=50, description="Số đánh giá mỗi trang"),
    db: AsyncSession = Depends(get_db),
):
    """Xem danh sách các đánh giá nhận được của một Hero kèm điểm trung bình."""
    return await rating_service.get_user_ratings(db, user_id, page, per_page)
