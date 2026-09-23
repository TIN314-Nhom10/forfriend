# Task 10 — Friend System & Real-time Chat

## Mục tiêu
Xây dựng hệ thống kết bạn (request/accept/reject), nhắn tin riêng real-time qua WebSocket, và quản lý conversations.

## Phụ thuộc
- Task 03 (Auth)
- Task 07 (Room System) — cần WebSocket ConnectionManager đã có
- Task 02 (Models) — `Friendship`, `Message`

## Tham chiếu
- [03-api-design.md](../03-api-design.md) — Section 6 (Friends), Section 7 (Messages), Section 8 (WebSocket)
- [01-architecture.md](../01-architecture.md) — Sequence diagram 2.4

## Yêu cầu chi tiết

### 10.1. Pydantic Schemas

```python
# Friends
class FriendResponse(BaseModel):
    friendship_id: UUID
    friend: UserBrief
    is_online: bool
    since: datetime

class FriendRequestResponse(BaseModel):
    friendship_id: UUID
    from_user: UserBrief
    created_at: datetime

# Messages
class MessageResponse(BaseModel):
    id: UUID
    sender_id: UUID
    content: str
    is_mine: bool
    is_read: bool
    created_at: datetime

class ConversationResponse(BaseModel):
    friend: UserBrief
    is_online: bool
    last_message: MessageResponse | None
    unread_count: int

class MessageListResponse(BaseModel):
    items: list[MessageResponse]
    has_more: bool
```

### 10.2. Friend Service

- `send_request(db, requester_id, addressee_id)`
  - Validate: không tự add mình, chưa có friendship record (cả 2 chiều)
  - Insert friendship (status=pending)
  - **WebSocket event** tới addressee

- `accept_request(db, friendship_id, user_id)`
  - Validate: user là addressee, status=pending
  - Update status → accepted
  - **WebSocket event** tới requester

- `reject_request(db, friendship_id, user_id)`
  - Validate: user là addressee
  - Update status → rejected

- `remove_friend(db, user_id, friend_id)`
  - Delete friendship record
  
- `get_friends(db, user_id) -> list[FriendResponse]`
  - Query friendships where status=accepted
  - Kèm is_online (check WebSocket connections)
  
- `get_friend_requests(db, user_id) -> list[FriendRequestResponse]`
  - Incoming pending requests

- `are_friends(db, user_id_1, user_id_2) -> bool`
  - Helper: kiểm tra 2 user có phải bạn bè không
  - Dùng để validate trước khi nhắn tin

### 10.3. Message Service

- `get_conversations(db, user_id) -> list[ConversationResponse]`
  - Danh sách bạn bè có tin nhắn, sắp xếp theo tin nhắn mới nhất
  - Kèm unread_count và last_message

- `get_messages(db, user_id, friend_id, before, limit) -> MessageListResponse`
  - Lịch sử tin nhắn 1-1, cursor-based pagination (dùng `before` timestamp)
  - Default limit = 50
  - Validate: 2 user phải là bạn bè

- `create_message(db, sender_id, receiver_id, content) -> MessageResponse`
  - Validate: phải là bạn bè
  - Sanitize content
  - Insert message
  - Return message object

- `mark_read(db, user_id, friend_id)`
  - Update tất cả message từ friend_id tới user_id: is_read = true, read_at = now()

### 10.4. Chat WebSocket

Tạo `backend/app/websockets/chat.py`:

```python
@app.websocket("/ws/chat/{friend_id}")
async def ws_chat(
    websocket: WebSocket,
    friend_id: UUID,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    user = await verify_ws_token(token)
    
    # Validate friendship
    if not await friend_service.are_friends(db, user.id, friend_id):
        await websocket.close(code=4003, reason="Not friends")
        return

    await chat_manager.connect(str(user.id), str(friend_id), websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "message":
                # Save to DB
                msg = await message_service.create_message(
                    db, user.id, friend_id, data["content"]
                )
                # Forward to friend if online
                await chat_manager.send_to_user(str(friend_id), {
                    "type": "message",
                    "content": msg.content,
                    "message_id": str(msg.id),
                    "created_at": msg.created_at.isoformat(),
                })
                # Also send notification if friend not in this chat
                await notification_manager.send_to_user(str(friend_id), {
                    "type": "new_message",
                    "data": {
                        "from": str(user.id),
                        "from_name": user.name,
                        "from_avatar": user.avatar_id,
                        "content": msg.content[:100],  # Preview
                        "created_at": msg.created_at.isoformat(),
                    }
                })
            
            elif data["type"] == "typing":
                await chat_manager.send_to_user(str(friend_id), {
                    "type": "typing"
                })
            
            elif data["type"] == "stop_typing":
                await chat_manager.send_to_user(str(friend_id), {
                    "type": "stop_typing"
                })
            
            elif data["type"] == "read":
                await message_service.mark_read(db, user.id, friend_id)
                await chat_manager.send_to_user(str(friend_id), {
                    "type": "read",
                    "read_at": datetime.utcnow().isoformat(),
                })
                
    except WebSocketDisconnect:
        await chat_manager.disconnect(str(user.id), str(friend_id))
```

### 10.5. Online Status

Dùng WebSocket ConnectionManager để track online status:
- Khi user connect `/ws/notifications` → mark online
- Khi disconnect → mark offline
- Broadcast `user_online` / `user_offline` events tới friends

### 10.6. Friend Router

```python
router = APIRouter(prefix="/api/v1/friends", tags=["friends"])

@router.post("/request/{user_id}", status_code=201)
@router.post("/accept/{friendship_id}")
@router.post("/reject/{friendship_id}")
@router.delete("/{user_id}")
@router.get("/", response_model=list[FriendResponse])
@router.get("/requests", response_model=list[FriendRequestResponse])
```

### 10.7. Message Router

```python
router = APIRouter(prefix="/api/v1/messages", tags=["messages"])

@router.get("/conversations", response_model=list[ConversationResponse])
@router.get("/{friend_id}", response_model=MessageListResponse)
@router.post("/{friend_id}/read")
```

### 10.8. Tests

**Friends:**
- Test send request thành công
- Test send request tới chính mình → 400
- Test send request trùng → 409
- Test accept → status = accepted
- Test reject → status = rejected
- Test accept bởi non-addressee → 403
- Test get friends list
- Test get incoming requests
- Test remove friend

**Messages:**
- Test get conversations sorted by latest message
- Test get messages history (pagination)
- Test mark read
- Test unread_count đúng
- Test nhắn tin cho non-friend → 400

**WebSocket:**
- Test chat WS: send message → friend receives
- Test typing indicator
- Test online/offline status events

## Tiêu chí hoàn thành

- [ ] Friend request/accept/reject flow hoạt động
- [ ] Danh sách bạn bè kèm is_online
- [ ] Chat WebSocket real-time: gửi + nhận tin nhắn
- [ ] Typing indicator hoạt động
- [ ] Message history với cursor pagination
- [ ] Conversations list sorted by latest
- [ ] Unread count đúng
- [ ] Mark read hoạt động
- [ ] Online/offline status broadcast tới friends
- [ ] Notification khi nhận tin nhắn mới
- [ ] Chỉ nhắn tin được với bạn bè
- [ ] Tests pass
