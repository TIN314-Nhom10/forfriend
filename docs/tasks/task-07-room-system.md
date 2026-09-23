# Task 07 — Room System (Phòng học)

## Mục tiêu
Xây dựng hệ thống tạo phòng, lobby hiển thị phòng theo category, request/approve/reject flow, và WebSocket notifications cho host.

## Phụ thuộc
- Task 03 (Auth)
- Task 02 (Models) — `Room`, `RoomCategory`, `RoomParticipant`
- Task 06 (Matching) — `calculate_room_score` (optional, có thể tích hợp sau)

## Tham chiếu
- [03-api-design.md](../03-api-design.md) — Section 4 (Rooms)
- [01-architecture.md](../01-architecture.md) — Sequence diagram 2.3

## Yêu cầu chi tiết

### 7.1. Pydantic Schemas

```python
class RoomCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    topic: str = Field(min_length=3, max_length=200)
    category_id: UUID
    max_participants: int = Field(default=10, ge=2, le=20)

class RoomResponse(BaseModel):
    id: UUID
    name: str
    room_code: str
    topic: str
    category: RoomCategoryResponse
    host: UserBrief
    status: str  # waiting | active | closed
    max_participants: int
    current_participants: int
    created_at: datetime

class RoomDetailResponse(RoomResponse):
    participants: list[ParticipantResponse]

class ParticipantResponse(BaseModel):
    user: UserBrief
    status: str
    joined_at: datetime | None

class RoomCategoryResponse(BaseModel):
    id: UUID
    name: str
    icon: str
    color: str
    active_rooms_count: int | None = None

class RoomListResponse(BaseModel):
    items: list[RoomResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
```

### 7.2. Room Service

- `create_room(db, user_id, data: RoomCreate) -> RoomResponse`
  - Validate category_id tồn tại
  - Generate room_code duy nhất (6 chars, alphanumeric uppercase)
  - Insert room + tạo participant entry cho host (status=accepted)
  
- `get_rooms(db, page, per_page, category_id, status, search) -> RoomListResponse`
  - Filter theo category, status, search text
  - Default: chỉ show "waiting" và "active"
  - Join với host info

- `get_room_detail(db, room_id) -> RoomDetailResponse`
  - Include danh sách participants

- `get_categories(db) -> list[RoomCategoryResponse]`
  - Kèm `active_rooms_count` cho mỗi category

- `request_join(db, room_id, user_id) -> ParticipantResponse`
  - Validate: phòng active/waiting, chưa đầy, user chưa request
  - Insert participant (status=pending)
  - **Trigger WebSocket** tới host

- `approve_request(db, room_id, host_id, target_user_id)`
  - Validate: caller là host
  - Update participant status → accepted
  - Increment current_participants
  - **Trigger WebSocket** tới target user

- `reject_request(db, room_id, host_id, target_user_id)`
  - Validate: caller là host
  - Update participant status → rejected

- `leave_room(db, room_id, user_id)`
  - Update participant status → left, set left_at
  - Decrement current_participants
  - Nếu host rời → close room

- `close_room(db, room_id, host_id)`
  - Validate: caller là host
  - Update room status → closed
  - Set closed_at
  - **Trigger WebSocket** tới tất cả participants: "room_closed"

### 7.3. Room Code Generator

```python
import secrets
import string

def generate_room_code(length: int = 6) -> str:
    """Generate mã phòng ngẫu nhiên, ví dụ: 'XK3M7P'."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
```

Cần check unique trong DB trước khi dùng.

### 7.4. WebSocket Handler cho Room Events

Tạo `backend/app/websockets/notifications.py`:

```python
class ConnectionManager:
    """Quản lý WebSocket connections theo user_id."""
    
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    async def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
    
    async def send_to_user(self, user_id: str, event: dict):
        if user_id in self.active_connections:
            for ws in self.active_connections[user_id]:
                await ws.send_json(event)
```

WebSocket endpoint:
```python
@app.websocket("/ws/notifications")
async def ws_notifications(websocket: WebSocket, token: str = Query(...)):
    user = await verify_ws_token(token)
    await manager.connect(str(user.id), websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle ping/pong
    except WebSocketDisconnect:
        await manager.disconnect(str(user.id), websocket)
```

### 7.5. Room Router

```python
router = APIRouter(prefix="/api/v1/rooms", tags=["rooms"])

@router.post("/", response_model=RoomResponse, status_code=201)
@router.get("/", response_model=RoomListResponse)
@router.get("/categories", response_model=list[RoomCategoryResponse])
@router.get("/{room_id}", response_model=RoomDetailResponse)
@router.post("/{room_id}/request", status_code=201)
@router.post("/{room_id}/approve/{user_id}")
@router.post("/{room_id}/reject/{user_id}")
@router.post("/{room_id}/leave")
@router.post("/{room_id}/close")
```

### 7.6. Tests

- Test tạo phòng → room_code unique
- Test get rooms (filter by category, search)
- Test get categories với active_rooms_count
- Test request join flow
- Test approve → participant status = accepted
- Test reject → participant status = rejected
- Test request vào phòng đã đầy → 400
- Test request khi đã request rồi → 409
- Test approve bởi non-host → 403
- Test leave room → current_participants giảm
- Test host leave → room closed
- Test close room → tất cả participants notified
- Test WebSocket nhận được event khi có request mới

## Tiêu chí hoàn thành

- [ ] CRUD phòng hoạt động
- [ ] Room code unique 6 chars
- [ ] Request → Approve/Reject flow hoạt động
- [ ] WebSocket notifications gửi tới đúng user
- [ ] Categories API trả active_rooms_count
- [ ] Leave room xử lý đúng (host leave = close)
- [ ] Close room notify tất cả participants
- [ ] Pagination + filters hoạt động
- [ ] Tests pass
