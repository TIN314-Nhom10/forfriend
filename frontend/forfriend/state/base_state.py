"""Base State cho toàn bộ Reflex app ForFriend với LocalStorage đồng bộ và hỗ trợ đa ngôn ngữ ENG/VIE."""
from typing import Optional
import httpx
import reflex as rx

API_BASE_URL = "http://localhost:8000/api/v1"
WS_BASE_URL = "ws://localhost:8000"


class BaseState(rx.State):
    """Trạng thái cơ sở chứa JWT token (LocalStorage), ngôn ngữ, và tiện ích gọi API."""

    # LocalStorage lưu trữ session người dùng và tự động đồng bộ qua mọi tab/trang
    token: str = rx.LocalStorage("", name="ff_token", sync=True)
    user_id: str = rx.LocalStorage("", name="ff_user_id", sync=True)
    user_name: str = rx.LocalStorage("", name="ff_user_name", sync=True)
    avatar_id: str = rx.LocalStorage("1", name="ff_avatar_id", sync=True)
    user_school: str = rx.LocalStorage("", name="ff_user_school", sync=True)
    user_city: str = rx.LocalStorage("", name="ff_user_city", sync=True)

    # Language: English UI by default
    lang: str = rx.LocalStorage("eng", name="ff_lang", sync=True)

    # Toast notifications
    toast_message: str = ""
    toast_type: str = "success"  # success, error, info
    show_toast: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        """Kiểm tra người dùng đã đăng nhập hay chưa."""
        return bool(self.token and self.token.strip())

    @rx.var
    def my_avatar_src(self) -> str:
        """Đường dẫn ảnh avatar an toàn cho profile người dùng hiện tại."""
        raw = str(self.avatar_id or "1").replace('"', '').replace("'", "").strip()
        clean = raw.replace("avatar_", "").replace("avatar-", "").replace(".png", "").lstrip("0")
        if not clean:
            clean = "1"
        try:
            cid = int(clean)
            if cid < 1 or cid > 15:
                cid = 1
        except Exception:
            cid = 1
        return f"/avatars/avatar_{cid}.png"

    @rx.var
    def is_vietnamese(self) -> bool:
        """System UI is English."""
        return False

    def toggle_lang(self):
        """Optional language toggle (defaults to English)."""
        pass

    def set_lang(self, new_lang: str):
        """Thiết lập ngôn ngữ cụ thể."""
        self.lang = new_lang

    def auth_headers(self) -> dict:
        """Tạo header Authorization chuẩn Bearer JWT."""
        headers = {"Content-Type": "application/json"}
        if self.token and self.token.strip():
            headers["Authorization"] = f"Bearer {self.token.strip()}"
        return headers

    def set_user_session(self, token: str, user: dict):
        """Gán thông tin session đăng nhập đồng bộ."""
        self.token = token
        self.user_id = str(user.get("id", ""))
        self.user_name = user.get("name", "")
        self.avatar_id = str(user.get("avatar_id", 1))
        self.user_school = user.get("school", "") or ""
        self.user_city = user.get("city", "") or ""

    async def login_as_demo(self):
        """Đăng nhập nhanh 1-Click bằng tài khoản sinh viên demo sẵn có."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/auth/login",
                    json={
                        "email": "nguyenvana@ftu.edu.vn",
                        "password": "Password123!",
                    },
                )
            if resp.status_code == 200:
                data = resp.json()
                token = data.get("access_token", "")
                user = data.get("user", {})
                self.set_user_session(token, user)
                self.notify("Logged in as Demo User (Nguyen Van A - FTU)!", "success")
            else:
                self.notify("Could not log in as demo user.", "error")
        except Exception as e:
            self.notify(f"Login error: {str(e)}", "error")

    def notify(self, message: str, toast_type: str = "success"):
        """Kích hoạt thông báo toast."""
        self.toast_message = message
        self.toast_type = toast_type
        self.show_toast = True

    def dismiss_toast(self):
        """Tắt thông báo toast."""
        self.show_toast = False
        self.toast_message = ""

    def logout_user(self):
        """Xóa sạch token và đăng xuất."""
        self.token = ""
        self.user_id = ""
        self.user_name = ""
        self.avatar_id = "1"
        self.user_school = ""
        self.user_city = ""
        return rx.redirect("/login")
