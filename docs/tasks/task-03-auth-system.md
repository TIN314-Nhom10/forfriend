# Task 03 — Authentication System

## Mục tiêu
Xây dựng hệ thống đăng ký, đăng nhập, JWT token management, và auth middleware cho FastAPI.

## Phụ thuộc
- Task 01 (Project Setup)
- Task 02 (Database Models) — cần model `User`, `UserSubject`

## Tham chiếu
- [03-api-design.md](../03-api-design.md) — Section 1 (Authentication)
- [01-architecture.md](../01-architecture.md) — Section 6 (Security)

## Yêu cầu chi tiết

### 3.1. Pydantic Schemas

Tạo `backend/app/schemas/auth.py`:
```python
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars, có ít nhất 1 chữ hoa + 1 số
    name: str  # 2-100 chars
    date_of_birth: date
    major: str
    school: str
    city: str
    district: str | None = None
    address_detail: str | None = None
    avatar_id: int = Field(ge=1, le=15, default=1)
    bio: str | None = None
    subjects: list[str] = []  # Danh sách môn học

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserBrief

class RefreshRequest(BaseModel):
    refresh_token: str
```

### 3.2. Auth Utilities

Tạo `backend/app/utils/auth.py`:

- `hash_password(password: str) -> str` — bcrypt hash
- `verify_password(plain: str, hashed: str) -> bool`
- `create_access_token(data: dict) -> str` — JWT, expire 15 min
- `create_refresh_token(data: dict) -> str` — JWT, expire 7 days
- `decode_token(token: str) -> dict` — Decode + validate
- `get_current_user(token: str = Depends(oauth2_scheme)) -> User` — FastAPI dependency

### 3.3. Auth Service

Tạo `backend/app/services/auth_service.py`:

- `register(db, data: RegisterRequest, student_id_file, cv_file) -> TokenResponse`
  - Validate email unique
  - Hash password
  - Insert user + subjects
  - Handle file uploads (student ID, CV) nếu có
  - Return tokens

- `login(db, data: LoginRequest) -> TokenResponse`
  - Find user by email
  - Verify password
  - Return tokens

- `refresh(db, data: RefreshRequest) -> dict`
  - Validate refresh token
  - Return new access token

### 3.4. Auth Router

Tạo `backend/app/routers/auth.py`:

```python
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=201)
@router.post("/login", response_model=TokenResponse)
@router.post("/refresh")
```

### 3.5. Auth Middleware / Dependency

Tạo dependency `get_current_user` có thể dùng trong mọi router:
```python
# Trong router khác
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    ...
```

### 3.6. Rate Limiting

Áp dụng rate limit cho auth endpoints:
- `/auth/register`: 5 req/phút/IP
- `/auth/login`: 10 req/phút/IP
- `/auth/refresh`: 30 req/phút/IP

### 3.7. Tests

Tạo `backend/tests/test_auth.py`:
- Test register thành công
- Test register email trùng → 409
- Test register password yếu → 400
- Test login thành công
- Test login sai password → 401
- Test refresh token
- Test access endpoint không có token → 401
- Test access endpoint token hết hạn → 401

## Tiêu chí hoàn thành

- [ ] Đăng ký tạo user + hash password + trả JWT tokens
- [ ] Đăng nhập verify password + trả tokens
- [ ] Refresh token hoạt động đúng
- [ ] `get_current_user` dependency hoạt động
- [ ] Rate limiting active trên auth endpoints
- [ ] Password validation (min 8, ít nhất 1 uppercase + 1 digit)
- [ ] Tất cả tests pass
- [ ] Swagger UI `/docs` hiển thị đúng schema
