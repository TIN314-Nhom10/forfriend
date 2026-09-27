"""Register State quản lý quá trình tạo Hero và chọn Avatar Chibi."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL


class RegisterState(BaseState):
    """Trạng thái đăng ký thành viên."""

    name: str = ""
    email: str = ""
    password: str = ""
    school: str = "Đại học Ngoại Thương Hà Nội"
    city: str = "Hà Nội"
    selected_avatar_id: int = 1
    error_message: str = ""
    is_loading: bool = False

    def set_name(self, val: str):
        self.name = val

    def set_email(self, val: str):
        self.email = val

    def set_password(self, val: str):
        self.password = val

    def set_school(self, val: str):
        self.school = val

    def set_city(self, val: str):
        self.city = val

    def set_avatar(self, avatar_id: int):
        """Chọn avatar chibi (1-15)."""
        self.selected_avatar_id = int(avatar_id)

    async def handle_register(self):
        """Gửi yêu cầu tạo tài khoản Hero tới Backend."""
        if not self.name.strip() or not self.email.strip() or not self.password.strip():
            self.error_message = "Please fill in Full Name, Email, and Password!"
            return

        if len(self.password) < 8:
            self.error_message = "Password must be at least 8 characters with uppercase, numbers and symbols!"
            return

        self.is_loading = True
        self.error_message = ""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/auth/register",
                    json={
                        "name": self.name.strip(),
                        "email": self.email.strip(),
                        "password": self.password,
                        "school": self.school.strip(),
                        "city": self.city.strip(),
                        "avatar_id": self.selected_avatar_id,
                        "date_of_birth": "2003-01-01",
                        "major": "General",
                    },
                )
                if resp.status_code == 201:
                    # Tự động đăng nhập
                    login_resp = await client.post(
                        f"{API_BASE_URL}/auth/login",
                        json={"email": self.email.strip(), "password": self.password},
                    )
                    if login_resp.status_code == 200:
                        ldata = login_resp.json()
                        token = ldata.get("access_token", "")
                        user = ldata.get("user", {})
                        base_state = await self.get_state(BaseState)
                        base_state.set_user_session(token, user)
                        self.token = token
                        self.user_id = str(user.get("id", ""))
                        self.user_name = user.get("name", "")
                        self.avatar_id = str(user.get("avatar_id", self.selected_avatar_id))
                        self.user_school = user.get("school", "") or ""
                        self.user_city = user.get("city", "") or ""
                        self.notify("Account created! Welcome to ForFriend!", "success")
                        return rx.redirect("/feed")
                    else:
                        self.notify("Registration successful! Please log in to start.", "success")
                        return rx.redirect("/login")
                else:
                    err = resp.json()
                    detail = err.get("detail", "Registration failed!")
                    if isinstance(detail, list) and len(detail) > 0:
                        detail = detail[0].get("msg", "Invalid registration data")
                    self.error_message = str(detail)
        except Exception as e:
            self.error_message = f"Cannot connect to server: {str(e)}"
        finally:
            self.is_loading = False
