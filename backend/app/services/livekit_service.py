import json
import logging
from typing import Optional
from livekit import api

from app.config import settings

logger = logging.getLogger(__name__)


class LiveKitService:
    """Service tích hợp LiveKit Server SDK cấp quyền và tạo token WebRTC cho phòng học."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or settings.LIVEKIT_API_KEY or "devkey"
        self.api_secret = (
            api_secret
            or settings.LIVEKIT_API_SECRET
            or "secret_dev_32_bytes_long_forfriend_livekit_key!"
        )
        self.url = url or settings.LIVEKIT_URL

    def generate_token(
        self,
        room_name: str,
        participant_identity: str,
        participant_name: str,
        avatar_id: int = 1,
        is_host: bool = False,
    ) -> str:
        """
        Tạo LiveKit access token cho participant (WebRTC JWT).
        
        Args:
            room_name: Mã phòng học (room_code)
            participant_identity: UUID của user dạng string
            participant_name: Tên hiển thị của Hero
            avatar_id: ID của chibi avatar
            is_host: True nếu là Host (bật room_admin và can_publish_data)
        """
        token = api.AccessToken(self.api_key, self.api_secret)
        token.with_identity(str(participant_identity))
        token.with_name(participant_name)
        token.with_metadata(
            json.dumps({"avatar_id": avatar_id, "is_host": is_host}, ensure_ascii=False)
        )

        grants = api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        )

        # Host có thêm quyền quản trị phòng (kick/mute) và gửi data stream
        if is_host:
            grants.room_admin = True
            grants.can_publish_data = True

        token.with_grants(grants)
        return token.to_jwt()

    async def close_room(self, room_name: str) -> None:
        """Đóng phòng học trên LiveKit Cloud (an toàn nếu không kết nối được server)."""
        if not self.url or "your-app" in self.url:
            return
        try:
            room_client = api.RoomServiceClient(self.url, self.api_key, self.api_secret)
            await room_client.delete_room(api.DeleteRoomRequest(room=room_name))
            await room_client.close()
            logger.info(f"LiveKit room {room_name} deleted on server.")
        except Exception as e:
            logger.warning(f"LiveKit delete_room failed for {room_name}: {e}")


livekit_service = LiveKitService()
