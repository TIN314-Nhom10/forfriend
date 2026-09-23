# Task 09 — Rating System (Đánh giá bạn học)

## Mục tiêu
Xây dựng hệ thống đánh giá bạn học 1–5 sao sau khi rời phòng, cập nhật avg_rating của user.

## Phụ thuộc
- Task 07 (Room System) — cần Room + RoomParticipant đã hoạt động
- Task 03 (Auth)
- Task 02 (Models) — `Rating`

## Tham chiếu
- [03-api-design.md](../03-api-design.md) — Section 5 (Ratings)

## Yêu cầu chi tiết

### 9.1. Pydantic Schemas

```python
class RatingCreate(BaseModel):
    ratee_id: UUID
    room_id: UUID
    stars: int = Field(ge=1, le=5)
    comment: str | None = Field(None, max_length=500)

class RatingResponse(BaseModel):
    id: UUID
    rater: UserBrief
    ratee: UserBrief
    room_id: UUID
    stars: int
    comment: str | None
    created_at: datetime

class UserRatingsResponse(BaseModel):
    items: list[RatingResponse]
    total: int
    avg_rating: float
    page: int
    per_page: int
```

### 9.2. Rating Service

- `create_rating(db, rater_id, data: RatingCreate) -> RatingResponse`

  **Validation rules:**
  - rater_id ≠ ratee_id (không tự rate mình)
  - Cả rater và ratee phải là participant (status=accepted hoặc left) của room_id
  - Mỗi cặp (rater, ratee, room) chỉ rate 1 lần → 409 nếu đã rate
  - Room phải tồn tại

  **Side effects:**
  - Update `user.avg_rating` và `user.total_ratings` cho ratee
  - Công thức: 
    ```
    new_total = old_total + 1
    new_avg = ((old_avg * old_total) + new_stars) / new_total
    ```

- `get_user_ratings(db, user_id, page, per_page) -> UserRatingsResponse`
  - Trả danh sách ratings mà user nhận được
  - Sắp xếp theo created_at DESC

- `get_pending_ratings(db, user_id, room_id) -> list[UserBrief]`
  - Trả danh sách users trong phòng mà current user chưa rate
  - Dùng cho UI popup sau khi rời phòng

### 9.3. Rating Router

```python
router = APIRouter(prefix="/api/v1/ratings", tags=["ratings"])

@router.post("/", response_model=RatingResponse, status_code=201)
async def create_rating(...)

@router.get("/pending/{room_id}", response_model=list[UserBrief])
async def get_pending_ratings(...)
```

```python
# Trong user router
@router.get("/{user_id}/ratings", response_model=UserRatingsResponse)
async def get_user_ratings(...)
```

### 9.4. Tích hợp với Leave Room

Khi user gọi `POST /rooms/{id}/leave`:
1. Update participant status → left
2. Response kèm thông tin: "Bạn có thể đánh giá các bạn học trong phòng"
3. Frontend hiện popup rating

### 9.5. Tests

- Test rate thành công → stars lưu đúng, avg_rating cập nhật
- Test tự rate mình → 400
- Test rate người không cùng phòng → 400
- Test rate trùng (cùng rater + ratee + room) → 409
- Test avg_rating tính đúng sau nhiều lần rate
- Test get pending ratings trả đúng danh sách chưa rate
- Test get user ratings phân trang đúng
- Test stars ngoài range (0 hoặc 6) → 400

## Tiêu chí hoàn thành

- [ ] Create rating với đầy đủ validation
- [ ] avg_rating + total_ratings cập nhật atomic
- [ ] Pending ratings API hoạt động (cho UI popup)
- [ ] Get user ratings phân trang
- [ ] Không thể tự rate mình
- [ ] Không thể rate trùng
- [ ] Chỉ rate được người cùng phòng
- [ ] Tests pass
