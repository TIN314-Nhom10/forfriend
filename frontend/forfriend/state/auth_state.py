"""Auth State quản lý đăng nhập và phiên làm việc của người dùng."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL


class AuthState(BaseState):
    """Trạng thái đăng nhập."""

    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    is_loading: bool = False

    def set_login_email(self, val: str):
        self.login_email = val

    def set_login_password(self, val: str):
        self.login_password = val

    def fill_demo(self, email: str = "nguyenvana@ftu.edu.vn", password: str = "Password123!"):
        """Điền nhanh tài khoản demo có sẵn."""
        self.login_email = email
        self.login_password = password
        self.login_error = ""

    async def handle_login(self):
        """Xử lý đăng nhập với API Backend."""
        if not self.login_email.strip() or not self.login_password.strip():
            self.login_error = "Please enter both Email and Password!"
            return

        self.is_loading = True
        self.login_error = ""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/auth/login",
                    json={
                        "email": self.login_email.strip(),
                        "password": self.login_password,
                    },
                )
            if resp.status_code == 200:
                data = resp.json()
                token = data.get("access_token", "")
                user = data.get("user", {})
                base_state = await self.get_state(BaseState)
                base_state.set_user_session(token, user)
                self.token = token
                self.user_id = str(user.get("id", ""))
                self.user_name = user.get("name", "")
                self.avatar_id = str(user.get("avatar_id", 1))
                self.user_school = user.get("school", "") or ""
                self.user_city = user.get("city", "") or ""
                self.login_password = ""
                self.notify("Login successful! Welcome back!", "success")
                return rx.redirect("/feed")
            else:
                err = resp.json()
                detail = err.get("detail", "Invalid email or password!")
                if isinstance(detail, list) and len(detail) > 0:
                    detail = detail[0].get("msg", "Invalid credentials")
                self.login_error = str(detail)
        except Exception as e:
            self.login_error = f"Cannot connect to server: {str(e)}"
        finally:
            self.is_loading = False

    def logout(self):
        """Đăng xuất người dùng."""
        return self.logout_user()
