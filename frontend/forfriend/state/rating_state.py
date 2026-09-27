"""Rating State quản lý popup đánh giá đồng đội sau khi rời phòng học."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL
from .models import TeammateItem


class RatingState(BaseState):
    """Trạng thái đánh giá 1-5 sao."""

    show_modal: bool = False
    pending_room_id: str = ""
    pending_users: list[TeammateItem] = []

    selected_user_id: str = ""
    selected_user_name: str = ""
    selected_user_avatar: int = 1

    stars: int = 5
    comment: str = "Great study buddy, very cooperative!"
    is_submitting: bool = False

    def set_comment(self, val: str):
        self.comment = val

    def close_modal(self):
        """Đóng popup đánh giá."""
        self.show_modal = False
        self.pending_users = []
        self.selected_user_id = ""

    def set_stars(self, count: int):
        """Chọn số sao 1-5."""
        self.stars = int(count)

    def select_user(self, user_id: str, name: str, avatar: int):
        """Chọn thành viên muốn đánh giá."""
        self.selected_user_id = str(user_id)
        self.selected_user_name = name
        self.selected_user_avatar = int(avatar)

    async def open_for_room(self, room_id: str):
        """Lấy danh sách thành viên cùng phòng cần đánh giá."""
        self.pending_room_id = str(room_id)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/ratings/pending/{room_id}",
                    headers=self.auth_headers(),
                )
            if resp.status_code == 200:
                raw_users = resp.json()
                self.pending_users = [
                    TeammateItem(
                        id=str(u.get("id", "")),
                        name=u.get("name", "Study Buddy"),
                        avatar_id=int(u.get("avatar_id", 1)),
                        school=u.get("school", ""),
                    )
                    for u in raw_users
                ]
                if self.pending_users:
                    first = self.pending_users[0]
                    self.selected_user_id = first.id
                    self.selected_user_name = first.name
                    self.selected_user_avatar = first.avatar_id
                    self.show_modal = True
        except Exception:
            pass

    async def submit_rating(self):
        """Gửi đánh giá lên máy chủ."""
        if not self.selected_user_id or not self.pending_room_id:
            return

        self.is_submitting = True
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/ratings/",
                    json={
                        "reviewee_id": self.selected_user_id,
                        "room_id": self.pending_room_id,
                        "stars": self.stars,
                        "comment": self.comment.strip(),
                    },
                    headers=self.auth_headers(),
                )
            if resp.status_code == 201:
                self.notify(f"★ Sent {self.stars} stars review to {self.selected_user_name}!", "success")
                self.pending_users = [u for u in self.pending_users if u.id != self.selected_user_id]
                if self.pending_users:
                    next_u = self.pending_users[0]
                    self.selected_user_id = next_u.id
                    self.selected_user_name = next_u.name
                    self.selected_user_avatar = next_u.avatar_id
                else:
                    self.show_modal = False
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Could not submit rating")), "warning")
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")
        finally:
            self.is_submitting = False
