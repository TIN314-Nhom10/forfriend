import json
from collections import defaultdict
from typing import Any, Dict, Optional, Set, Tuple
from fastapi import WebSocket


class ConnectionManager:
    """
    In-Memory WebSocket ConnectionManager.
    Quản lý kết nối WebSocket theo room và user ID, thay thế hoàn toàn Redis Pub/Sub.
    """

    def __init__(self) -> None:
        # room_id -> set of WebSockets
        self.room_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        # user_id -> set of WebSockets (hỗ trợ 1 user mở nhiều tab)
        self.user_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        # websocket -> (user_id, room_id | None)
        self.connection_meta: Dict[WebSocket, Dict[str, Optional[str]]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        user_id: str,
        room_id: Optional[str] = None,
    ) -> None:
        """Chấp nhận kết nối và lưu vào danh mục quản lý."""
        await websocket.accept()
        self.user_connections[user_id].add(websocket)
        if room_id:
            self.room_connections[room_id].add(websocket)
        self.connection_meta[websocket] = {"user_id": user_id, "room_id": room_id}

    def disconnect(self, websocket: WebSocket) -> None:
        """Hủy đăng ký kết nối khi client ngắt kết nối."""
        meta = self.connection_meta.pop(websocket, None)
        if meta:
            user_id = meta.get("user_id")
            room_id = meta.get("room_id")

            if user_id and user_id in self.user_connections:
                self.user_connections[user_id].discard(websocket)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]

            if room_id and room_id in self.room_connections:
                self.room_connections[room_id].discard(websocket)
                if not self.room_connections[room_id]:
                    del self.room_connections[room_id]

    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket) -> None:
        """Gửi message trực tiếp tới 1 kết nối WebSocket cụ thể."""
        await websocket.send_text(json.dumps(message, ensure_ascii=False))

    async def send_to_user(self, user_id: str, message: Dict[str, Any]) -> int:
        """
        Gửi message tới tất cả các session đang mở của 1 user.
        Trả về số kết nối nhận được message.
        """
        payload = json.dumps(message, ensure_ascii=False)
        targets = list(self.user_connections.get(user_id, []))
        sent_count = 0
        for ws in targets:
            try:
                await ws.send_text(payload)
                sent_count += 1
            except Exception:
                self.disconnect(ws)
        return sent_count

    async def broadcast_to_room(
        self,
        room_id: str,
        message: Dict[str, Any],
        exclude: Optional[WebSocket] = None,
    ) -> int:
        """
        Broadcast message tới tất cả các client đang trong 1 phòng.
        Tùy chọn bỏ qua người gửi (exclude).
        """
        payload = json.dumps(message, ensure_ascii=False)
        targets = list(self.room_connections.get(room_id, []))
        sent_count = 0
        for ws in targets:
            if exclude is not None and ws == exclude:
                continue
            try:
                await ws.send_text(payload)
                sent_count += 1
            except Exception:
                self.disconnect(ws)
        return sent_count

    async def broadcast_to_users(
        self,
        user_ids: list[str],
        message: Dict[str, Any],
    ) -> int:
        """
        Broadcast message tới danh sách các user ID cụ thể.
        Trả về tổng số kết nối đã nhận được message.
        """
        total_sent = 0
        for uid in user_ids:
            total_sent += await self.send_to_user(uid, message)
        return total_sent

    def is_user_online(self, user_id: str) -> bool:
        """Kiểm tra user có ít nhất 1 kết nối WebSocket đang hoạt động không."""
        return user_id in self.user_connections and len(self.user_connections[user_id]) > 0


class ChatConnectionManager:
    """Quản lý các kết nối WebSocket trong các phòng chat 1-1 (In-Memory RAM, 0% Redis)."""

    def __init__(self) -> None:
        # Key: (user_id, friend_id) -> WebSocket
        self.active_chats: Dict[Tuple[str, str], WebSocket] = {}

    async def connect(self, user_id: str, friend_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_chats[(user_id, friend_id)] = websocket

    def disconnect(self, user_id: str, friend_id: str) -> None:
        self.active_chats.pop((user_id, friend_id), None)

    async def send_to_chat(
        self, from_user_id: str, to_user_id: str, data: Dict[str, Any]
    ) -> bool:
        """Gửi trực tiếp tin nhắn tới cửa sổ chat của bạn bè nếu họ đang mở khung chat này."""
        friend_socket = self.active_chats.get((to_user_id, from_user_id))
        if friend_socket:
            try:
                await friend_socket.send_text(json.dumps(data, ensure_ascii=False))
                return True
            except Exception:
                self.disconnect(to_user_id, from_user_id)
        return False

    def is_chat_open(self, user_id: str, friend_id: str) -> bool:
        return (user_id, friend_id) in self.active_chats


# Singleton manager instance dùng chung cho ứng dụng
connection_manager = ConnectionManager()
notification_manager = connection_manager
chat_manager = ChatConnectionManager()
