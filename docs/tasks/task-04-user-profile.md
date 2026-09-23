# Task 04 — User Profile & File Upload

## Mục tiêu
API quản lý profile user (xem, sửa), upload file (thẻ sinh viên, CV), và chọn avatar chibi.

## Phụ thuộc
- Task 03 (Auth System) — cần `get_current_user` dependency

## Tham chiếu
- [03-api-design.md](../03-api-design.md) — Section 2 (Users), Section 9 (File Upload)

## Yêu cầu chi tiết

### 4.1. Pydantic Schemas

```python
class UserProfile(BaseModel):
    """Full profile response."""
    id: UUID
    email: str
    name: str
    date_of_birth: date
    major: str
    school: str
    city: str
    district: str | None
    avatar_id: int
    bio: str | None
    avg_rating: float
    total_ratings: int
    subjects: list[str]
    created_at: datetime

class UserPublic(BaseModel):
    """Public profile (người khác xem)."""
    id: UUID
    name: str
    school: str
    major: str
    avatar_id: int
    bio: str | None
    avg_rating: float
    total_ratings: int
    subjects: list[str]

class UserBrief(BaseModel):
    """Brief info cho embed trong post, room..."""
    id: UUID
    name: str
    avatar_id: int
    school: str
    avg_rating: float

class UserUpdate(BaseModel):
    """Partial update."""
    name: str | None = None
    major: str | None = None
    school: str | None = None
    city: str | None = None
    district: str | None = None
    address_detail: str | None = None
    avatar_id: int | None = Field(None, ge=1, le=15)
    bio: str | None = None
    subjects: list[str] | None = None
```

### 4.2. User Service

- `get_profile(db, user_id) -> UserProfile`
- `get_public_profile(db, user_id) -> UserPublic`
- `update_profile(db, user_id, data: UserUpdate) -> UserProfile`
  - Nếu `subjects` thay đổi: xóa cũ, insert mới
- `update_avatar(db, user_id, avatar_id: int) -> UserProfile`

### 4.3. File Upload Service

Tạo `backend/app/services/upload_service.py`:

- `upload_student_id(file: UploadFile) -> str`
  - Validate: image only (jpg, png, webp), max 5MB
  - Lưu vào `uploads/student-ids/{uuid}.{ext}`
  - Return URL path

- `upload_cv(file: UploadFile) -> str`
  - Validate: PDF only, max 10MB
  - Lưu vào `uploads/cvs/{uuid}.pdf`
  - Return URL path

- Đảm bảo tạo thư mục `uploads/` nếu chưa có
- Static file serving trong FastAPI cho `/uploads/`

### 4.4. User Router

```python
router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/me", response_model=UserProfile)
@router.put("/me", response_model=UserProfile)
@router.get("/{user_id}", response_model=UserPublic)
```

### 4.5. Upload Router

```python
router = APIRouter(prefix="/api/v1/upload", tags=["upload"])

@router.post("/student-id")
@router.post("/cv")
```

### 4.6. Tests

- Test get own profile
- Test update profile (partial update)
- Test change avatar (1–15 valid, 0 or 16 → 400)
- Test view other user's public profile
- Test view non-existent user → 404
- Test upload student ID (valid image)
- Test upload student ID (file quá lớn → 400)
- Test upload CV (valid PDF)
- Test upload CV (file không phải PDF → 400)

## Tiêu chí hoàn thành

- [ ] GET /users/me trả full profile
- [ ] PUT /users/me update partial fields
- [ ] GET /users/{id} trả public profile
- [ ] Upload student ID: validate type + size, lưu file, trả URL
- [ ] Upload CV: validate type + size, lưu file, trả URL
- [ ] Static files serving hoạt động
- [ ] Avatar ID validate range 1–15
- [ ] Tests pass
