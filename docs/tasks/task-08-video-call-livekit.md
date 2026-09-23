# Task 08 — Video Call Integration (LiveKit)

## Mục tiêu
Tích hợp LiveKit để enable video call trong phòng học. Backend cấp token, Frontend kết nối LiveKit Cloud qua WebRTC.

## Phụ thuộc
- Task 07 (Room System) — cần approve flow hoạt động
- Task 03 (Auth)

## Tham chiếu
- [01-architecture.md](../01-architecture.md) — Sequence diagram 2.3
- LiveKit docs: https://docs.livekit.io/

## Yêu cầu chi tiết

### 8.1. LiveKit Service (Backend)

Tạo `backend/app/services/livekit_service.py`:

```python
from livekit import api

class LiveKitService:
    def __init__(self, api_key: str, api_secret: str, url: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.url = url

    def generate_token(
        self,
        room_name: str,
        participant_identity: str,
        participant_name: str,
        avatar_id: int,
        is_host: bool = False,
    ) -> str:
        """
        Generate LiveKit access token cho participant.
        
        Args:
            room_name: Mã phòng (room_code)
            participant_identity: user_id (string)
            participant_name: Tên hiển thị
            avatar_id: Avatar ID (gửi qua metadata)
            is_host: Host có quyền mute/kick
        
        Returns:
            JWT token string
        """
        token = api.AccessToken(self.api_key, self.api_secret)
        token.with_identity(participant_identity)
        token.with_name(participant_name)
        token.with_metadata(json.dumps({
            "avatar_id": avatar_id,
            "is_host": is_host,
        }))

        grants = api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        )

        # Host có thêm quyền admin
        if is_host:
            grants.room_admin = True
            grants.can_publish_data = True

        token.with_grants(grants)
        return token.to_jwt()

    async def create_room(self, room_name: str, max_participants: int):
        """Tạo room trên LiveKit server (optional, room auto-create khi join)."""
        room_service = api.RoomServiceClient(self.url, self.api_key, self.api_secret)
        await room_service.create_room(
            api.CreateRoomRequest(
                name=room_name,
                empty_timeout=300,  # Tự đóng sau 5 phút trống
                max_participants=max_participants,
            )
        )

    async def close_room(self, room_name: str):
        """Xóa room trên LiveKit server."""
        room_service = api.RoomServiceClient(self.url, self.api_key, self.api_secret)
        await room_service.delete_room(api.DeleteRoomRequest(room=room_name))
```

### 8.2. Tích hợp vào Room Flow

Modify approve flow trong `RoomService`:

```python
async def approve_request(self, db, room_id, host_id, target_user_id):
    # ... existing logic ...
    
    # Generate LiveKit token cho user được approve
    livekit_token = self.livekit_service.generate_token(
        room_name=room.room_code,
        participant_identity=str(target_user_id),
        participant_name=user.name,
        avatar_id=user.avatar_id,
        is_host=False,
    )
    
    # Gửi token qua WebSocket
    await self.ws_manager.send_to_user(str(target_user_id), {
        "type": "room_approved",
        "data": {
            "room_id": str(room_id),
            "livekit_token": livekit_token,
            "livekit_url": settings.LIVEKIT_URL,
        }
    })
```

Thêm endpoint lấy token (cho host hoặc reconnect):
```python
@router.get("/{room_id}/token")
async def get_livekit_token(
    room_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Lấy LiveKit token. Chỉ cho participant đã accepted."""
    # Validate user là participant accepted hoặc host
    # Generate và return token
```

### 8.3. Frontend LiveKit — Reflex Custom Component

> **Note**: Video call là **ngoại lệ duy nhất** cần JS. Tạo Reflex Custom Component để wrap LiveKit JS SDK, giữ phần logic Python tối đa.

Cài JS SDK (Reflex tự quản lý nếu dùng `_build_hooks`):
```bash
# Chạy một lần dưới .web/ do Reflex generate
npm install @livekit/components-react livekit-client
```

Tạo `forfriend/components/livekit_component.py`:
```python
import reflex as rx
from reflex.components.component import NoSSRComponent

class LiveKitRoom(NoSSRComponent):
    """
    Reflex Custom Component wrap @livekit/components-react.
    Đây là ngoại lệ duy nhất có JS trong dự án.
    """
    library = "@livekit/components-react"
    tag = "LiveKitRoom"

    # Props — Python type hints, map sang JS props
    server_url: rx.Var[str]
    token: rx.Var[str]
    connect: rx.Var[bool] = True
    audio: rx.Var[bool] = True
    video: rx.Var[bool] = True


class VideoConference(NoSSRComponent):
    """Grid layout video của LiveKit."""
    library = "@livekit/components-react"
    tag = "VideoConference"


class RoomAudioRenderer(NoSSRComponent):
    """Audio renderer — bắt buộc cho audio hoạt động."""
    library = "@livekit/components-react"
    tag = "RoomAudioRenderer"


# Cách dùng trong page Python:
# def video_call_page():
#     return LiveKitRoom(
#         server_url=VideoCallState.livekit_url,
#         token=VideoCallState.livekit_token,
#         children=[VideoConference(), RoomAudioRenderer()],
#     )
```

Cấu trúc component video:
```
forfriend/components/video/
├── livekit_component.py   # Custom Component bridge Python→JS
├── control_bar.py         # Nút mic/cam/leave (Python thuần)
├── participant_list.py    # Sidebar danh sách (Python thuần)
└── pending_requests.py    # Host approve UI (Python thuần)
```

### 8.4. LiveKit Cloud Setup

Hướng dẫn setup (đưa vào README):
1. Đăng ký tại https://cloud.livekit.io
2. Tạo project → lấy API Key + Secret
3. Thêm vào `.env`:
   ```
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   LIVEKIT_URL=wss://your-project.livekit.cloud
   ```

### 8.5. Tests

- Test generate token trả valid JWT
- Test token chứa đúng identity, room, metadata
- Test host token có room_admin = true
- Test non-host token không có room_admin
- Test get token endpoint: accepted participant → 200
- Test get token endpoint: non-participant → 403
- Test get token endpoint: pending participant → 403

## Tiêu chí hoàn thành

- [ ] LiveKitService generate token đúng format
- [ ] Approve flow tự động cấp LiveKit token qua WebSocket
- [ ] GET /{room_id}/token endpoint hoạt động
- [ ] Host token có quyền admin
- [ ] Metadata chứa avatar_id
- [ ] Close room gọi LiveKit delete room
- [ ] Hướng dẫn setup LiveKit Cloud trong README
- [ ] Tests pass
