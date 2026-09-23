# Task 05 — Post Feed (Bảng tin)

## Mục tiêu
CRUD bài đăng tìm bạn học + API lấy feed cơ bản (chưa có matching algorithm, sẽ bổ sung ở Task 06).

## Phụ thuộc
- Task 03 (Auth) — `get_current_user`
- Task 02 (Models) — `Post`, `PostTag`

## Tham chiếu
- [03-api-design.md](../03-api-design.md) — Section 3 (Posts)

## Yêu cầu chi tiết

### 5.1. Pydantic Schemas

```python
class PostCreate(BaseModel):
    content: str = Field(min_length=10, max_length=2000)
    study_type: Literal["online", "offline"]
    location: str | None = None  # Bắt buộc nếu offline
    preferred_school: str | None = None
    study_date: datetime | None = None
    max_people: int = Field(default=5, ge=2, le=20)
    tags: list[str] = Field(default=[], max_length=5)  # Max 5 tags

    @model_validator(mode="after")
    def validate_location(self):
        if self.study_type == "offline" and not self.location:
            raise ValueError("Location bắt buộc cho học offline")
        return self

class PostUpdate(BaseModel):
    content: str | None = Field(None, min_length=10, max_length=2000)
    study_type: Literal["online", "offline"] | None = None
    location: str | None = None
    study_date: datetime | None = None
    max_people: int | None = Field(None, ge=2, le=20)
    tags: list[str] | None = Field(None, max_length=5)

class PostResponse(BaseModel):
    id: UUID
    content: str
    study_type: str
    location: str | None
    preferred_school: str | None
    study_date: datetime | None
    max_people: int
    author: UserBrief
    tags: list[str]
    relevance_score: float | None = None  # Sẽ có sau Task 06
    created_at: datetime

class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
```

### 5.2. Post Service

- `create_post(db, user_id, data: PostCreate) -> PostResponse`
  - Sanitize content (bleach)
  - Insert post + tags
  
- `get_feed(db, user_id, page, per_page, study_type, tag) -> PostListResponse`
  - Lấy bài active, sắp xếp theo `created_at DESC` (mặc định)
  - Filter theo `study_type` và `tag` nếu có
  - Phân trang offset-based
  - **Note**: Matching score sẽ bổ sung ở Task 06

- `get_post(db, post_id) -> PostResponse`

- `update_post(db, user_id, post_id, data: PostUpdate) -> PostResponse`
  - Chỉ author mới được sửa
  - Nếu tags thay đổi: xóa cũ insert mới

- `delete_post(db, user_id, post_id)`
  - Soft delete: set `is_active = false`
  - Chỉ author mới được xóa

### 5.3. Post Router

```python
router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=201)
@router.get("/feed", response_model=PostListResponse)
@router.get("/{post_id}", response_model=PostResponse)
@router.put("/{post_id}", response_model=PostResponse)
@router.delete("/{post_id}", status_code=204)
```

### 5.4. Tests

- Test tạo bài đăng online
- Test tạo bài đăng offline thiếu location → 400
- Test feed trả về đúng format, phân trang
- Test filter theo study_type
- Test filter theo tag
- Test update bài (chỉ author)
- Test update bài bởi người khác → 403
- Test delete bài (soft delete)
- Test get bài đã delete → 404
- Test content sanitization (XSS prevention)

## Tiêu chí hoàn thành

- [ ] CRUD bài đăng hoạt động đầy đủ
- [ ] Feed phân trang đúng
- [ ] Filter hoạt động
- [ ] Soft delete hoạt động
- [ ] Content sanitize (bleach)
- [ ] Validation: offline phải có location, max 5 tags
- [ ] Chỉ author mới sửa/xóa bài mình
- [ ] Tests pass
