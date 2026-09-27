"""Profile State quản lý thông tin Hero, đổi avatar, tải lên thẻ SV & CV, và lịch sử đánh giá."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL
from .models import ReviewItem


class ProfileState(BaseState):
    """Trạng thái Hồ sơ Hero."""

    profile_data: dict = {}
    ratings_history: list[ReviewItem] = []
    is_editing: bool = False
    is_loading: bool = False

    # Edit form
    edit_name: str = ""
    edit_bio: str = ""
    edit_school: str = ""
    edit_city: str = ""
    edit_subjects_input: str = ""

    # Uploads
    upload_msg: str = ""
    is_uploading: bool = False

    def set_edit_name(self, val: str):
        self.edit_name = val

    def set_edit_bio(self, val: str):
        self.edit_bio = val

    def set_edit_school(self, val: str):
        self.edit_school = val

    def set_edit_city(self, val: str):
        self.edit_city = val

    def set_edit_subjects_input(self, val: str):
        self.edit_subjects_input = val

    def toggle_edit(self):
        """Bật/tắt chế độ sửa thông tin."""
        self.is_editing = not self.is_editing
        if self.is_editing and self.profile_data:
            self.edit_name = self.profile_data.get("name", "")
            self.edit_bio = self.profile_data.get("bio", "") or ""
            self.edit_school = self.profile_data.get("school", "") or ""
            self.edit_city = self.profile_data.get("city", "") or ""
            subs = self.profile_data.get("subjects", [])
            self.edit_subjects_input = ", ".join(subs)

    async def load_profile(self):
        """Tải thông tin chi tiết hồ sơ cá nhân."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.is_loading = False
            return

        headers = {"Authorization": f"Bearer {token}"}
        self.is_loading = True
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Profile
                resp = await client.get(
                    f"{API_BASE_URL}/users/me",
                    headers=headers,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    has_id_card = bool(data.get("student_id_card_url"))
                    self.profile_data = {
                        "id": str(data.get("id", "")),
                        "name": data.get("name", "Student"),
                        "email": data.get("email", ""),
                        "avatar_id": int(data.get("avatar_id", 1)),
                        "school": data.get("school", "Not updated"),
                        "city": data.get("city", "Not updated"),
                        "bio": data.get("bio", "No bio provided yet."),
                        "avg_rating": float(data.get("avg_rating", 5.0)),
                        "total_ratings": int(data.get("total_ratings", 0)),
                        "is_verified": bool(data.get("is_verified") or has_id_card),
                        "student_id_url": data.get("student_id_card_url"),
                        "cv_url": data.get("cv_url"),
                        "subjects": data.get("subjects", []),
                    }
                    self.avatar_id = str(data.get("avatar_id", 1))
                    self.user_name = data.get("name", "")

                # 2. Ratings received
                r_resp = await client.get(
                    f"{API_BASE_URL}/ratings/me",
                    headers=headers,
                )
                if r_resp.status_code == 200:
                    r_data = r_resp.json()
                    items = r_data.get("items", [])
                    formatted = []
                    for r in items:
                        rev = r.get("reviewer") or {}
                        formatted.append(ReviewItem(
                            stars=int(r.get("stars", 5)),
                            comment=r.get("comment", ""),
                            reviewer_name=rev.get("name", "Study Buddy"),
                            reviewer_avatar_id=int(rev.get("avatar_id", 1)),
                            created_at=str(r.get("created_at", "")[:10]),
                        ))
                    self.ratings_history = formatted
        except Exception as e:
            self.notify(f"Error loading profile: {str(e)}", "error")
        finally:
            self.is_loading = False

    async def save_profile(self):
        """Lưu cập nhật thông tin cá nhân."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to update profile!", "error")
            return

        subs = [s.strip() for s in self.edit_subjects_input.split(",") if s.strip()]
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.put(
                    f"{API_BASE_URL}/users/me",
                    json={
                        "name": self.edit_name.strip(),
                        "bio": self.edit_bio.strip(),
                        "school": self.edit_school.strip(),
                        "city": self.edit_city.strip(),
                        "subjects": subs,
                    },
                    headers=headers,
                )
            if resp.status_code == 200:
                self.is_editing = False
                self.notify("Profile updated successfully!", "success")
                await self.load_profile()
            else:
                self.notify("Could not update profile!", "error")
        except Exception as e:
            self.notify(f"Error: {str(e)}", "error")

    async def change_avatar(self, new_avatar_id: int):
        """Đổi avatar đại diện."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to change avatar!", "error")
            return

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.put(
                    f"{API_BASE_URL}/users/me/avatar",
                    json={"avatar_id": int(new_avatar_id)},
                    headers=headers,
                )
            if resp.status_code == 200:
                self.avatar_id = str(new_avatar_id)
                self.notify(f"Selected Avatar #{new_avatar_id}!", "success")
                await self.load_profile()
        except Exception as e:
            self.notify(f"Error changing avatar: {str(e)}", "error")

    async def handle_student_id_upload(self, files: list[rx.UploadFile]):
        """Upload ảnh thẻ sinh viên xác thực."""
        if not files:
            return

        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to upload student ID!", "error")
            return

        upload_file = files[0]
        self.is_uploading = True
        try:
            content = await upload_file.read()
            async with httpx.AsyncClient(timeout=20.0) as client:
                files_payload = {
                    "file": (upload_file.name, content, upload_file.content_type)
                }
                headers = {"Authorization": f"Bearer {token}"}
                resp = await client.post(
                    f"{API_BASE_URL}/users/me/upload-student-id",
                    files=files_payload,
                    headers=headers,
                )
            if resp.status_code in (200, 201):
                resp_data = resp.json()
                msg = resp_data.get("message") or "Student ID verified and uploaded successfully!"
                self.notify(msg, "success")
                await self.load_profile()
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Error uploading student ID")), "error")
        except Exception as e:
            self.notify(f"Upload error: {str(e)}", "error")
        finally:
            self.is_uploading = False

    async def handle_cv_upload(self, files: list[rx.UploadFile]):
        """Upload file CV PDF."""
        if not files:
            return

        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to upload CV!", "error")
            return

        upload_file = files[0]
        self.is_uploading = True
        try:
            content = await upload_file.read()
            async with httpx.AsyncClient(timeout=20.0) as client:
                files_payload = {
                    "file": (upload_file.name, content, upload_file.content_type)
                }
                headers = {"Authorization": f"Bearer {token}"}
                resp = await client.post(
                    f"{API_BASE_URL}/users/me/upload-cv",
                    files=files_payload,
                    headers=headers,
                )
            if resp.status_code in (200, 201):
                self.notify("CV uploaded successfully!", "success")
                await self.load_profile()
            else:
                err = resp.json()
                self.notify(str(err.get("detail", "Error uploading CV")), "error")
        except Exception as e:
            self.notify(f"Upload error: {str(e)}", "error")
        finally:
            self.is_uploading = False
