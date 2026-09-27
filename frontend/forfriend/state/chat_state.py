"""Chat State quản lý kết bạn, danh sách bạn bè và nhắn tin thời gian thực 1-1."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL
from .models import FriendItem, FriendRequestItem, MessageItem


class ChatState(BaseState):
    """Trạng thái bạn bè và trò chuyện."""

    friends: list[FriendItem] = []
    friend_requests: list[FriendRequestItem] = []
    conversations: list[dict] = []

    active_friend_id: str = ""
    active_friend_name: str = ""
    active_friend_avatar: int = 1
    active_friend_online: bool = False

    messages: list[MessageItem] = []
    message_input: str = ""
    is_loading: bool = False
    is_sending: bool = False

    def set_message_input(self, val: str):
        self.message_input = val

    async def handle_key_down(self, key: str):
        """Xử lý nhấn phím Enter để gửi tin nhắn."""
        if key == "Enter":
            await self.send_message()

    async def load_chat_page(self):
        """Khởi tạo trang Quán trọ bạn bè."""
        await self.load_friends()
        await self.load_friend_requests()
        await self.load_conversations()
        if self.friends and not self.active_friend_id:
            first = self.friends[0]
            await self.select_friend(
                first.user_id,
                first.name,
                first.avatar_id,
                first.is_online,
            )

    async def load_friends(self):
        """Tải danh sách bạn bè kèm trạng thái online."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.friends = []
            return

        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/friends/",
                    headers=headers,
                )
            if resp.status_code == 200:
                raw = resp.json()
                formatted = []
                for item in raw:
                    f = item.get("friend") or {}
                    formatted.append(FriendItem(
                        friendship_id=str(item.get("friendship_id", "")),
                        user_id=str(f.get("id", "")),
                        name=f.get("name", "Ally"),
                        avatar_id=int(f.get("avatar_id", 1)),
                        school=f.get("school", ""),
                        rating=float(f.get("rating", 5.0)),
                        is_online=bool(item.get("is_online", False)),
                        since=str(item.get("since", "")[:10]),
                    ))
                self.friends = formatted
        except Exception:
            pass

    async def load_friend_requests(self):
        """Tải lời mời kết bạn đang chờ duyệt."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.friend_requests = []
            return

        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/friends/requests",
                    headers=headers,
                )
            if resp.status_code == 200:
                raw = resp.json()
                formatted = []
                for req in raw:
                    u = req.get("from_user") or {}
                    formatted.append(FriendRequestItem(
                        friendship_id=str(req.get("friendship_id", "")),
                        user_id=str(u.get("id", "")),
                        name=u.get("name", "Student"),
                        avatar_id=int(u.get("avatar_id", 1)),
                        school=u.get("school", ""),
                    ))
                self.friend_requests = formatted
        except Exception:
            pass

    async def load_conversations(self):
        """Tải danh sách cuộc trò chuyện gần đây."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.conversations = []
            return

        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/messages/conversations",
                    headers=headers,
                )
            if resp.status_code == 200:
                self.conversations = resp.json()
        except Exception:
            pass

    async def select_friend(self, friend_id: str, name: str, avatar: int, online: bool):
        """Chọn bạn bè để trò chuyện."""
        self.active_friend_id = str(friend_id)
        self.active_friend_name = name
        self.active_friend_avatar = int(avatar)
        self.active_friend_online = bool(online)
        await self.load_messages()

    async def load_messages(self):
        """Tải lịch sử chat với bạn bè hiện tại."""
        if not self.active_friend_id:
            return

        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            return

        headers = {"Authorization": f"Bearer {token}"}
        self.is_loading = True
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/messages/{self.active_friend_id}",
                    headers=headers,
                )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                formatted = []
                for m in items:
                    formatted.append(MessageItem(
                        id=str(m.get("id", "")),
                        sender_id=str(m.get("sender_id", "")),
                        receiver_id=str(m.get("receiver_id", "")),
                        content=m.get("content", ""),
                        is_mine=bool(m.get("is_mine", False)),
                        is_read=bool(m.get("is_read", False)),
                        created_at=str(m.get("created_at", "")[11:16]),
                    ))
                self.messages = formatted
                # Đánh dấu đã đọc
                await client.post(
                    f"{API_BASE_URL}/messages/{self.active_friend_id}/read",
                    headers=headers,
                )
        except Exception as e:
            self.notify(f"Error loading messages: {str(e)}", "error")
        finally:
            self.is_loading = False

    async def send_message(self):
        """Gửi tin nhắn 1-1."""
        if not self.message_input.strip() or not self.active_friend_id:
            return

        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to chat!", "error")
            return

        text = self.message_input.strip()
        self.message_input = ""
        self.is_sending = True

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/messages/{self.active_friend_id}",
                    json={"content": text},
                    headers=headers,
                )
            if resp.status_code in (200, 201):
                await self.load_messages()
                await self.load_conversations()
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Could not send message")), "error")
        except Exception as e:
            self.notify(f"Error sending message: {str(e)}", "error")
        finally:
            self.is_sending = False

    async def send_friend_request(self, target_user_id: str):
        """Gửi lời mời kết bạn từ Bảng tin hoặc Hồ sơ."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to send friend requests!", "warning")
            return

        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/friends/request/{target_user_id}",
                    headers=headers,
                )
            if resp.status_code == 201:
                self.notify("⚔ Friend request sent!", "success")
                await self.load_friends()
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Could not send friend request")), "warning")
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")

    async def accept_request(self, friendship_id: str):
        """Chấp nhận lời mời kết bạn."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/friends/accept/{friendship_id}",
                    headers=headers,
                )
            if resp.status_code == 200:
                self.notify("✨ Successfully connected as study friends!", "success")
                await self.load_friends()
                await self.load_friend_requests()
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")

    async def reject_request(self, friendship_id: str):
        """Từ chối lời mời kết bạn."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/friends/reject/{friendship_id}",
                    headers=headers,
                )
            if resp.status_code == 200:
                self.notify("Friend request declined.", "info")
                await self.load_friend_requests()
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")

    async def remove_friend(self, friend_user_id: str):
        """Hủy kết bạn."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        headers = {"Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.delete(
                    f"{API_BASE_URL}/friends/{friend_user_id}",
                    headers=headers,
                )
            if resp.status_code == 200:
                self.notify("Friend removed.", "info")
                self.active_friend_id = ""
                await self.load_friends()
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")
