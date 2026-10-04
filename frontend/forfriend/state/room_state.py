"""Room State quản lý Sảnh phòng học (Adventure Zones) và LiveKit Video Call."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL
from .models import RoomItem, CategoryItem, KnockRequestItem


class RoomState(BaseState):
    """Trạng thái phòng học ảo và LiveKit WebRTC."""

    rooms: list[RoomItem] = []
    categories: list[CategoryItem] = []
    selected_category_id: str = ""
    search_query: str = ""
    is_loading: bool = False

    # Modal tạo phòng
    show_create_modal: bool = False
    new_room_title: str = ""
    new_room_topic: str = "Học nhóm ôn thi cuối kỳ"
    new_room_category_id: str = ""
    new_room_max: int = 6
    create_error: str = ""
    is_auth_error: bool = False

    # Trong phòng & Call
    current_room_id: str = ""
    current_room_title: str = ""
    current_room_host_id: str = ""
    is_host: bool = False
    livekit_token: str = ""
    livekit_url: str = "wss://forfriend-k8hok508.livekit.cloud"
    is_in_call: bool = False

    # Duyệt thành viên gõ cửa
    pending_requests: list[KnockRequestItem] = []
    show_approval_modal: bool = False

    def set_new_room_title(self, val: str):
        self.new_room_title = val

    def set_new_room_topic(self, val: str):
        self.new_room_topic = val

    def set_new_room_category_id(self, val: str):
        self.new_room_category_id = val

    def set_new_room_max(self, val: str):
        try:
            self.new_room_max = int(val)
        except Exception:
            self.new_room_max = 6

    def set_search_query(self, val: str):
        self.search_query = val

    def toggle_create_modal(self):
        """Mở/đóng popup tạo phòng."""
        self.show_create_modal = not self.show_create_modal
        self.create_error = ""

    def toggle_approval_modal(self):
        """Mở/đóng modal duyệt thành viên gõ cửa."""
        self.show_approval_modal = not self.show_approval_modal

    async def set_category(self, cat_id: str):
        """Chọn danh mục phòng học."""
        self.selected_category_id = "" if self.selected_category_id == cat_id else cat_id
        await self.load_rooms()

    async def load_lobby(self):
        """Khởi tạo Sảnh phòng học: Tải danh mục và phòng."""
        await self.load_categories()
        await self.load_rooms()

    async def load_categories(self):
        """Tải 10 danh mục phòng học có sẵn."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{API_BASE_URL}/rooms/categories")
            if resp.status_code == 200:
                raw = resp.json()
                self.categories = [
                    CategoryItem(
                        id=str(c.get("id", "")),
                        name=c.get("name", "Chung"),
                        code=c.get("code", "general"),
                        icon=c.get("icon", "🎮"),
                    )
                    for c in raw
                ]
                if self.categories and not self.new_room_category_id:
                    self.new_room_category_id = self.categories[0].id
        except Exception:
            pass

    async def load_rooms(self):
        """Tải danh sách phòng học đang mở."""
        self.is_loading = True
        params = {}
        if self.selected_category_id:
            params["category_id"] = self.selected_category_id
        if self.search_query.strip():
            params["search"] = self.search_query.strip()

        base_state = await self.get_state(BaseState)
        current_uid = str(base_state.user_id or self.user_id or "")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{API_BASE_URL}/rooms/", params=params)
            if resp.status_code == 200:
                data = resp.json()
                raw_rooms = data.get("items", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                formatted = []
                for r in raw_rooms:
                    if not isinstance(r, dict):
                        continue
                    host = r.get("host") or {}
                    cat = r.get("category") or {}
                    curr_p = int(r.get("current_participants", 1))
                    max_p = int(r.get("max_participants", 6))
                    formatted.append(RoomItem(
                        id=str(r.get("id", "")),
                        room_code=r.get("room_code", "ZONE-01"),
                        title=r.get("name") or r.get("title", "Adventure Zone"),
                        topic=r.get("topic", "") or "",
                        category_name=cat.get("name", "General") if isinstance(cat, dict) else "General",
                        category_icon=cat.get("icon", "🎮") if isinstance(cat, dict) else "🎮",
                        host_id=str(host.get("id", "")) if isinstance(host, dict) else "",
                        host_name=host.get("name", "Host") if isinstance(host, dict) else "Host",
                        host_avatar_id=int(host.get("avatar_id", 1)) if isinstance(host, dict) else 1,
                        current_participants=curr_p,
                        max_participants=max_p,
                        is_full=curr_p >= max_p,
                        is_my_room=bool(current_uid and str(host.get("id", "")) == current_uid) if isinstance(host, dict) else False,
                    ))
                self.rooms = formatted
        except Exception as e:
            self.notify(f"Error loading rooms: {str(e)}", "error")
        finally:
            self.is_loading = False

    async def create_room(self):
        """Tạo phòng học ảo mới."""
        self.create_error = ""
        self.is_auth_error = False
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()

        if not token:
            self.is_auth_error = True
            self.create_error = "⚠️ Bạn chưa đăng nhập. Vui lòng bấm Demo Login hoặc Đăng nhập để tạo phòng!"
            return

        if not self.new_room_title.strip():
            self.create_error = "Vui lòng nhập tên phòng học!"
            return

        cat_id = self.new_room_category_id or (self.categories[0].id if self.categories else "")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/rooms/",
                    json={
                        "name": self.new_room_title.strip(),
                        "title": self.new_room_title.strip(),
                        "topic": self.new_room_topic.strip(),
                        "category_id": cat_id,
                        "max_participants": int(self.new_room_max),
                    },
                    headers=base_state.auth_headers(),
                )
            if resp.status_code == 201:
                data = resp.json()
                room_id = str(data.get("id"))
                self.show_create_modal = False
                self.notify("Study room created! Entering zone...", "success")
                return await self.enter_room(room_id)
            elif resp.status_code == 401:
                self.is_auth_error = True
                self.create_error = "⚠️ Phiên đăng nhập (JWT) đã hết hạn. Vui lòng bấm Demo Login hoặc Đăng nhập lại!"
            else:
                err = resp.json()
                self.create_error = str(err.get("detail", "Failed to create room!"))
        except Exception as e:
            self.create_error = f"Error: {str(e)}"

    async def request_join(self, room_id: str):
        """Gửi yêu cầu gõ cửa xin vào phòng (Knock)."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to knock and join this room!", "warning")
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/rooms/{room_id}/request",
                    headers=base_state.auth_headers(),
                )
            if resp.status_code == 200:
                self.notify("🚪 Knock sent! Please wait for Host approval...", "info")
            elif resp.status_code == 401:
                self.notify("⚠️ Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!", "error")
            elif resp.status_code == 409:
                return await self.enter_room(room_id)
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Could not send knock request!")), "error")
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")

    async def fetch_livekit_token(self, room_id: str):
        """Lấy token LiveKit và chuẩn bị kết nối WebRTC."""
        self.is_loading = True
        base_state = await self.get_state(BaseState)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/rooms/{room_id}/token",
                    headers=base_state.auth_headers(),
                )
            if resp.status_code == 200:
                data = resp.json()
                self.current_room_id = str(room_id)
                self.livekit_token = data.get("livekit_token") or data.get("token", "")
                self.livekit_url = data.get("livekit_url") or data.get("url") or "wss://forfriend-k8hok508.livekit.cloud"
                self.is_host = bool(data.get("is_host", False))
                self.is_in_call = True
            elif resp.status_code == 401:
                self.notify("⚠️ Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại!", "error")
            elif resp.status_code == 403:
                self.notify("You haven't been approved by the Host yet. Waiting for approval...", "warning")
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Could not enter room")), "error")
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")
        finally:
            self.is_loading = False

    async def enter_room(self, room_id: str):
        """Chuyển hướng vào phòng học ảo."""
        self.current_room_id = str(room_id)
        return rx.redirect(f"/rooms/{room_id}")

    async def on_video_call_mount(self):
        """Tự động kiểm tra và lấy token LiveKit khi trang /rooms/[room_id] tải."""
        rid = self.router.page.params.get("room_id", "")
        if not rid:
            rid = self.current_room_id
        if not rid:
            return rx.redirect("/rooms")

        self.current_room_id = str(rid)
        await self.fetch_livekit_token(self.current_room_id)
        if self.is_host:
            await self.load_pending_requests()

    async def load_pending_requests(self):
        """Host lấy danh sách yêu cầu gõ cửa."""
        if not self.current_room_id or not self.is_host:
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/rooms/{self.current_room_id}/requests",
                    headers=self.auth_headers(),
                )
            if resp.status_code == 200:
                raw = resp.json()
                self.pending_requests = [
                    KnockRequestItem(
                        id=str(req.get("id", "")),
                        user_id=str((req.get("user") or {}).get("id", "")),
                        name=(req.get("user") or {}).get("name", "Student"),
                        avatar_id=int((req.get("user") or {}).get("avatar_id", 1)),
                        school=(req.get("user") or {}).get("school", ""),
                    )
                    for req in raw
                ]
        except Exception:
            pass

    async def approve_user(self, request_id: str):
        """Host phê duyệt thành viên."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/rooms/{self.current_room_id}/approve/{request_id}",
                    headers=self.auth_headers(),
                )
            if resp.status_code == 200:
                self.notify("Approved user into the room!", "success")
                await self.load_pending_requests()
        except Exception as e:
            self.notify(f"Approval error: {str(e)}", "error")

    async def reject_user(self, request_id: str):
        """Host từ chối thành viên."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/rooms/{self.current_room_id}/reject/{request_id}",
                    headers=self.auth_headers(),
                )
            if resp.status_code == 200:
                self.notify("Request declined.", "info")
                await self.load_pending_requests()
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")

    async def leave_room(self):
        """Rời khỏi phòng học và mở modal đánh giá."""
        room_id = self.current_room_id
        if room_id:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.post(
                        f"{API_BASE_URL}/rooms/{room_id}/leave",
                        headers=self.auth_headers(),
                    )
            except Exception:
                pass

        self.is_in_call = False
        self.livekit_token = ""
        self.current_room_id = ""
        self.notify("Left study room. Feel free to rate your study buddy!", "info")
        return rx.redirect("/rooms")
