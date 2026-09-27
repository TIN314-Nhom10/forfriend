"""Feed State quản lý Bảng tin Quest tìm bạn học và thuật toán matching."""
import httpx
import reflex as rx
from .base_state import BaseState, API_BASE_URL
from .models import PostItem


class FeedState(BaseState):
    """Trạng thái Bảng tin Quest."""

    posts: list[PostItem] = []
    filter_tag: str = ""
    filter_mode: str = "ALL"  # ALL, ONLINE, OFFLINE
    search_query: str = ""
    level_filter: str = "All Levels"
    timezone_filter: str = "All"
    is_loading: bool = False
    page: int = 1
    has_more: bool = False

    # Modal tạo Quest mới
    show_create_modal: bool = False
    new_title: str = ""
    new_content: str = ""
    new_tags_input: str = "Python, Math, AI"
    new_is_online: bool = True
    new_location: str = "Campus Library"
    create_error: str = ""

    # Modal chi tiết Quest
    show_details_modal: bool = False
    details_title: str = ""
    details_content: str = ""
    details_author_name: str = ""
    details_author_school: str = ""
    details_author_rating: float = 5.0
    details_author_avatar: int = 1
    details_author_id: str = ""
    details_tags: list[str] = []
    details_is_online: bool = True
    details_location: str = ""
    details_created_at: str = ""

    def view_quest_details(self, post: PostItem):
        self.details_title = post.title
        self.details_content = post.content
        self.details_author_name = post.author_name
        self.details_author_school = post.author_school
        self.details_author_rating = post.author_rating
        self.details_author_avatar = post.author_avatar_id
        self.details_author_id = post.author_id
        self.details_tags = post.tags
        self.details_is_online = post.is_online
        self.details_location = post.location
        self.details_created_at = post.created_at
        self.show_details_modal = True

    def close_quest_details(self):
        self.show_details_modal = False

    def share_quest(self, title: str):
        self.notify(f"Link copied to clipboard for: {title}!", "info")

    async def set_search_query(self, val: str):
        self.search_query = val
        await self.load_feed()

    def set_level_filter(self, val: str):
        self.level_filter = val

    def set_timezone_filter(self, val: str):
        self.timezone_filter = val

    async def on_subject_change(self, val: str):
        self.filter_tag = "" if val == "All Subjects" else val
        await self.load_feed()

    async def on_availability_change(self, val: str):
        self.filter_mode = "ALL" if val == "All" else val.upper()
        await self.load_feed()

    def set_new_title(self, val: str):
        self.new_title = val

    def set_new_content(self, val: str):
        self.new_content = val

    def set_new_tags_input(self, val: str):
        self.new_tags_input = val

    def set_new_location(self, val: str):
        self.new_location = val

    def set_new_is_online(self, val: bool):
        self.new_is_online = val

    def toggle_create_modal(self):
        """Đóng/mở modal tạo bài đăng."""
        self.show_create_modal = not self.show_create_modal
        self.create_error = ""

    async def set_filter_tag(self, tag: str):
        """Lọc theo môn học."""
        self.filter_tag = "" if self.filter_tag == tag else tag
        await self.load_feed()

    async def set_filter_mode(self, mode: str):
        """Lọc theo hình thức Online / Offline."""
        self.filter_mode = mode
        await self.load_feed()

    async def load_feed(self):
        """Tải danh sách bài đăng từ API Backend."""
        self.is_loading = True
        params = {"page": self.page, "limit": 20}
        if self.filter_tag:
            params["tag"] = self.filter_tag
        if self.filter_mode == "ONLINE":
            params["is_online"] = True
        elif self.filter_mode == "OFFLINE":
            params["is_online"] = False

        base_state = await self.get_state(BaseState)
        headers = base_state.auth_headers()

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{API_BASE_URL}/posts/feed",
                    params=params,
                    headers=headers,
                )
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                formatted = []
                my_id = str(base_state.user_id) if base_state.user_id else str(self.user_id)
                for p in items:
                    raw_content = p.get("content", "")
                    if "]" in raw_content and raw_content.startswith("["):
                        parts = raw_content.split("]", 1)
                        title = parts[0].replace("[", "").strip()
                        content = parts[1].strip()
                    else:
                        title = "Quest Học Tập"
                        content = raw_content

                    author = p.get("author") or {}
                    author_id = str(author.get("id", p.get("author_id", "")))
                    author_name = author.get("name", "Student")
                    author_avatar_id = int(author.get("avatar_id", 1))
                    author_school = author.get("school", "Đại học")
                    author_rating = float(author.get("avg_rating", 5.0))
                    match_val = float(p.get("relevance_score") or p.get("match_score") or 0.88)

                    formatted.append(PostItem(
                        id=str(p.get("id", "")),
                        title=title,
                        content=content,
                        is_online=p.get("study_type", "online") == "online",
                        location=p.get("location") or "Học Online",
                        author_id=author_id,
                        author_name=author_name,
                        author_avatar_id=author_avatar_id,
                        author_school=author_school,
                        author_rating=author_rating,
                        author_total_ratings=int(p.get("author_total_ratings", 5)),
                        tags=p.get("tags", []),
                        match_score=match_val,
                        match_pct=f"{int(match_val * 100)}%",
                        created_at=str(p.get("created_at", "")[:10]),
                        is_mine=author_id == my_id,
                    ))
                if self.search_query.strip():
                    q = self.search_query.strip().lower()
                    formatted = [
                        p for p in formatted
                        if q in p.title.lower()
                        or q in p.content.lower()
                        or q in p.author_name.lower()
                        or q in p.author_school.lower()
                        or any(q in t.lower() for t in p.tags)
                    ]
                self.posts = formatted
                self.has_more = bool(data.get("has_more", False))
        except Exception as e:
            self.notify(f"Error loading quests: {str(e)}", "error")
        finally:
            self.is_loading = False

    async def create_quest(self):
        """Đăng Quest tìm bạn học mới."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()

        if not token:
            self.create_error = "⚠️ Not authenticated! Please click '⚡ 1-Click Demo Login' above or log in to post a Quest."
            return

        if not self.new_title.strip() or not self.new_content.strip():
            self.create_error = "Please fill in Quest Title and Content!"
            return

        if not self.new_is_online and not self.new_location.strip():
            self.create_error = "Offline posts require a meeting location!"
            return

        tags_list = [t.strip() for t in self.new_tags_input.split(",") if t.strip()]
        full_content = f"[{self.new_title.strip()}] {self.new_content.strip()}"

        try:
            headers = base_state.auth_headers()
            payload = {
                "content": full_content,
                "study_type": "online" if self.new_is_online else "offline",
                "location": self.new_location.strip() if not self.new_is_online else None,
                "tags": tags_list[:5],
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{API_BASE_URL}/posts/",
                    json=payload,
                    headers=headers,
                )
            if resp.status_code == 201:
                self.show_create_modal = False
                self.new_title = ""
                self.new_content = ""
                self.create_error = ""
                self.notify("🚀 Quest published successfully to Board!", "success")
                await self.load_feed()
            else:
                err = resp.json()
                detail = err.get("detail", "Failed to create quest!")
                self.create_error = str(detail)
        except Exception as e:
            self.create_error = f"Connection error: {str(e)}"

    async def delete_quest(self, post_id: str):
        """Xóa bài đăng của chính mình."""
        base_state = await self.get_state(BaseState)
        token = (base_state.token or self.token or "").strip()
        if not token:
            self.notify("Please log in to delete this quest!", "error")
            return

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.delete(
                    f"{API_BASE_URL}/posts/{post_id}",
                    headers=headers,
                )
            if resp.status_code in (200, 204):
                self.notify("Quest removed from Board.", "info")
                await self.load_feed()
            else:
                try:
                    err = resp.json()
                    detail = err.get("detail", f"Error {resp.status_code}")
                except Exception:
                    detail = f"Error {resp.status_code}"
                self.notify(f"Could not delete Quest: {detail}", "error")
        except Exception as e:
            self.notify(f"Could not delete Quest: {str(e)}", "error")
