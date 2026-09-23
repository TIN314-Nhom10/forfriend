# Task 11 — Frontend: Game-style UI (Reflex — Python-first)

## Mục tiêu
Xây dựng toàn bộ giao diện với phong cách **web game retro / pixel art** sử dụng **Reflex** (Python framework). Bao gồm tất cả pages, components, State classes, và tích hợp LiveKit video call qua Reflex Custom Component.

> **Python-first**: ~95% code là Python thuần. JS duy nhất là LiveKit Custom Component (~30 dòng).

## Phụ thuộc
- Task 01 (Project Setup) — Reflex đã init
- Task 03–10 (Backend APIs) — Tất cả API endpoint đã sẵn sàng

## Tham chiếu
- [01-architecture.md](../01-architecture.md) — Section 4 (Frontend module design)
- [03-api-design.md](../03-api-design.md) — Tất cả endpoint + WebSocket
- Reflex docs: https://reflex.dev/docs/

---

## Yêu cầu chi tiết

### 11.1. Design System (CSS Variables + Theme)

Tạo `forfriend/styles/theme.py` — style dictionary dùng trong Reflex components:

```python
"""Game-style design system cho forfriend."""

# ===== COLOR PALETTE =====
colors = {
    "bg_primary": "#0a0a1a",       # Deep space black
    "bg_secondary": "#141432",      # Dark purple-blue
    "bg_card": "#1a1a3e",           # Card background
    "bg_card_hover": "#222255",     # Card hover
    "accent_primary": "#00ff88",    # Neon green
    "accent_secondary": "#ff6b9d",  # Pink
    "accent_tertiary": "#4ecdc4",   # Teal
    "accent_gold": "#ffd700",       # Gold stars
    "accent_purple": "#a855f7",     # Purple
    "text_primary": "#e0e0ff",      # Light blue-white
    "text_secondary": "#8888aa",    # Muted
    "border": "#333366",
    "border_glow": "#00ff8844",
    "danger": "#ff4444",
    "warning": "#ffaa00",
    "success": "#00ff88",
}

# ===== TYPOGRAPHY =====
fonts = {
    "pixel": "'Press Start 2P', monospace",
    "body": "'Inter', system-ui, sans-serif",
}

# ===== COMMON STYLES =====
pixel_border = {
    "border": f"3px solid {colors['border']}",
    "box_shadow": f"inset -2px -2px 0 {colors['bg_primary']}, inset 2px 2px 0 rgba(255,255,255,0.1)",
}

game_card_style = {
    "background": colors["bg_card"],
    "border": f"2px solid {colors['border']}",
    "border_radius": "8px",
    "padding": "24px",
    "transition": "all 250ms ease",
    "_hover": {
        "border_color": colors["accent_primary"],
        "box_shadow": f"0 8px 30px rgba(0, 255, 136, 0.15)",
        "transform": "translateY(-2px)",
    },
}

btn_primary_style = {
    "font_family": fonts["pixel"],
    "font_size": "10px",
    "padding": "8px 24px",
    "background": colors["accent_primary"],
    "color": colors["bg_primary"],
    "border": f"2px solid {colors['accent_primary']}",
    "cursor": "pointer",
    "text_transform": "uppercase",
    "letter_spacing": "1px",
    "transition": "all 150ms ease",
    "_hover": {
        "opacity": "0.85",
        "transform": "translateY(-1px)",
    },
}

btn_secondary_style = {
    **btn_primary_style,
    "background": "transparent",
    "color": colors["accent_primary"],
}

game_input_style = {
    "background": colors["bg_primary"],
    "border": f"2px solid {colors['border']}",
    "color": colors["text_primary"],
    "padding": "8px 16px",
    "font_family": fonts["body"],
    "font_size": "14px",
    "border_radius": "4px",
    "outline": "none",
    "_focus": {
        "border_color": colors["accent_primary"],
        "box_shadow": "0 0 8px rgba(0, 255, 136, 0.2)",
    },
}
```

Tạo `forfriend/styles/global.css` (CSS thuần cho animations và keyframes):

```css
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: #0a0a1a;
  color: #e0e0ff;
  font-family: 'Inter', sans-serif;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 136, 0.3); }
  50% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }
}

@keyframes pixel-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@keyframes slide-in-right {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.float { animation: float 3s ease-in-out infinite; }
.pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
.pixel-blink { animation: pixel-blink 1s step-end infinite; }
```

---

### 11.2. State Classes (Thay thế Hooks)

Trong Reflex, state management dùng Python class kế thừa `rx.State`.

#### `forfriend/state/auth_state.py`

```python
import reflex as rx
import httpx
from typing import Optional

class AuthState(rx.State):
    """Quản lý authentication state toàn app."""
    
    access_token: str = ""
    refresh_token: str = ""
    user_id: str = ""
    user_name: str = ""
    user_avatar_id: int = 1
    is_loading: bool = False
    error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return bool(self.access_token)

    async def login(self, form_data: dict):
        """Gọi POST /api/v1/auth/login."""
        self.is_loading = True
        self.error_message = ""
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://localhost:8000/api/v1/auth/login",
                    json=form_data,
                )
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                self.user_id = str(data["user"]["id"])
                self.user_name = data["user"]["name"]
                self.user_avatar_id = data["user"]["avatar_id"]
                return rx.redirect("/")
            else:
                self.error_message = resp.json().get("detail", "Đăng nhập thất bại")
        except Exception as e:
            self.error_message = "Lỗi kết nối server"
        finally:
            self.is_loading = False

    async def logout(self):
        self.access_token = ""
        self.refresh_token = ""
        return rx.redirect("/login")

    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}
```

#### `forfriend/state/feed_state.py`

```python
import reflex as rx
import httpx
from typing import list

class Post(rx.Base):
    id: str
    content: str
    author_name: str
    author_avatar_id: int
    author_rating: float
    match_score: float
    tags: list[str]
    created_at: str

class FeedState(AuthState):
    """Feed page state — kế thừa AuthState để dùng token."""
    
    posts: list[Post] = []
    is_loading: bool = False
    page: int = 1
    has_more: bool = True
    filter_tag: str = ""
    
    # New post form
    new_post_content: str = ""
    new_post_tags: list[str] = []
    show_create_modal: bool = False

    async def load_feed(self):
        """GET /api/v1/posts/feed"""
        self.is_loading = True
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "http://localhost:8000/api/v1/posts/feed",
                params={"page": self.page, "tag": self.filter_tag},
                headers=self._auth_headers(),
            )
        if resp.status_code == 200:
            data = resp.json()
            self.posts = [Post(**p) for p in data["items"]]
            self.has_more = data["has_more"]
        self.is_loading = False

    async def create_post(self):
        """POST /api/v1/posts"""
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://localhost:8000/api/v1/posts",
                json={"content": self.new_post_content, "tags": self.new_post_tags},
                headers=self._auth_headers(),
            )
        self.show_create_modal = False
        self.new_post_content = ""
        await self.load_feed()
```

#### `forfriend/state/room_state.py`

```python
import reflex as rx
import httpx

class Room(rx.Base):
    id: str
    name: str
    topic: str
    host_name: str
    host_avatar_id: int
    current_participants: int
    max_participants: int
    status: str

class RoomState(AuthState):
    rooms: list[Room] = []
    selected_category: str = ""
    livekit_token: str = ""
    livekit_url: str = ""
    is_in_call: bool = False

    async def load_rooms(self):
        """GET /api/v1/rooms"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "http://localhost:8000/api/v1/rooms",
                params={"topic": self.selected_category},
                headers=self._auth_headers(),
            )
        if resp.status_code == 200:
            self.rooms = [Room(**r) for r in resp.json()]

    async def request_join(self, room_id: str):
        """POST /api/v1/rooms/{id}/request"""
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://localhost:8000/api/v1/rooms/{room_id}/request",
                headers=self._auth_headers(),
            )

    def receive_livekit_token(self, token: str, url: str):
        """Gọi khi nhận được token từ WebSocket event 'room_approved'."""
        self.livekit_token = token
        self.livekit_url = url
        self.is_in_call = True
```

#### `forfriend/state/chat_state.py`

```python
import reflex as rx
import httpx

class Message(rx.Base):
    id: str
    sender_id: str
    sender_name: str
    sender_avatar_id: int
    content: str
    created_at: str
    is_mine: bool

class ChatState(AuthState):
    messages: list[Message] = []
    current_friend_id: str = ""
    message_input: str = ""
    is_typing: bool = False
    friend_is_typing: bool = False

    async def load_messages(self, friend_id: str):
        self.current_friend_id = friend_id
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"http://localhost:8000/api/v1/messages/{friend_id}",
                headers=self._auth_headers(),
            )
        if resp.status_code == 200:
            self.messages = [Message(**m) for m in resp.json()]

    async def send_message(self):
        if not self.message_input.strip():
            return
        # Gửi qua WebSocket (Reflex EventHandler kết nối ws)
        # hoặc POST REST API
        async with httpx.AsyncClient() as client:
            await client.post(
                f"http://localhost:8000/api/v1/messages/{self.current_friend_id}",
                json={"content": self.message_input},
                headers=self._auth_headers(),
            )
        self.message_input = ""
        await self.load_messages(self.current_friend_id)
```

---

### 11.3. Components (Python thuần)

#### `forfriend/components/common.py`

```python
import reflex as rx
from ..styles.theme import btn_primary_style, btn_secondary_style, game_card_style, colors

def game_button(text: str, on_click=None, variant: str = "primary") -> rx.Component:
    """Styled game button với hover effect."""
    style = btn_primary_style if variant == "primary" else btn_secondary_style
    return rx.button(
        text,
        on_click=on_click,
        style=style,
    )


def game_card(*children, **props) -> rx.Component:
    """Card container với pixel border style."""
    return rx.box(
        *children,
        style={**game_card_style, **props.get("style", {})},
        **{k: v for k, v in props.items() if k != "style"},
    )


def game_input(
    placeholder: str,
    value,
    on_change,
    input_type: str = "text",
) -> rx.Component:
    from ..styles.theme import game_input_style
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=input_type,
        style=game_input_style,
        width="100%",
    )


def pixel_title(text: str, size: str = "1.2rem") -> rx.Component:
    """Heading với pixel font + glow effect."""
    return rx.text(
        text,
        style={
            "font_family": "'Press Start 2P', monospace",
            "font_size": size,
            "color": colors["accent_primary"],
            "text_shadow": f"0 0 10px {colors['accent_primary']}",
        },
    )


def star_rating(rating: float, max_stars: int = 5) -> rx.Component:
    """Hiển thị sao vàng theo rating."""
    return rx.hstack(
        *[
            rx.text(
                "★",
                color=colors["accent_gold"] if i < round(rating) else colors["border"],
                font_size="1.2rem",
            )
            for i in range(max_stars)
        ],
        spacing="1",
    )


def avatar_display(avatar_id: int, size: str = "48px") -> rx.Component:
    """Hiển thị avatar chibi theo ID."""
    return rx.image(
        src=f"/assets/avatars/avatar-{avatar_id:02d}.png",
        width=size,
        height=size,
        style={
            "image_rendering": "pixelated",
            "border_radius": "50%",
        },
    )


def notification_toast(message: str, toast_type: str = "success") -> rx.Component:
    color_map = {
        "success": colors["success"],
        "error": colors["danger"],
        "info": colors["accent_tertiary"],
    }
    return rx.box(
        rx.text(message),
        style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "background": color_map.get(toast_type, colors["success"]),
            "color": colors["bg_primary"],
            "padding": "12px 20px",
            "border_radius": "4px",
            "font_family": "'Press Start 2P', monospace",
            "font_size": "10px",
            "animation": "slide-in-right 300ms ease",
            "z_index": "1000",
        },
    )
```

#### `forfriend/components/feed/post_card.py`

```python
import reflex as rx
from ..common import game_card, avatar_display, star_rating
from ...styles.theme import colors

def post_card(post) -> rx.Component:
    """Quest Card — hiển thị 1 bài đăng trong feed."""
    return game_card(
        rx.hstack(
            avatar_display(post.author_avatar_id),
            rx.vstack(
                rx.text(post.author_name, style={"font_weight": "bold", "color": colors["text_primary"]}),
                star_rating(post.author_rating),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.badge(
                f"⚡ Match {int(post.match_score * 100)}%",
                style={
                    "background": f"{colors['accent_primary']}22",
                    "color": colors["accent_primary"],
                    "border": f"1px solid {colors['accent_primary']}",
                    "font_family": "'Press Start 2P', monospace",
                    "font_size": "8px",
                    "padding": "4px 8px",
                },
            ),
            width="100%",
            align_items="center",
        ),
        rx.text(post.content, style={"color": colors["text_secondary"], "margin_top": "12px"}),
        rx.hstack(
            *[
                rx.badge(tag, style={"background": colors["bg_secondary"], "color": colors["accent_tertiary"]})
                for tag in post.tags
            ],
            spacing="2",
            margin_top="12px",
            flex_wrap="wrap",
        ),
        width="100%",
    )
```

#### `forfriend/components/room/room_card.py`

```python
import reflex as rx
from ..common import game_card, game_button, avatar_display
from ...styles.theme import colors
from ...state.room_state import RoomState

def room_card(room) -> rx.Component:
    """Phòng học card trong lobby."""
    is_full = room.current_participants >= room.max_participants
    return game_card(
        rx.hstack(
            avatar_display(room.host_avatar_id, size="40px"),
            rx.vstack(
                rx.text(room.name, font_weight="bold", color=colors["text_primary"]),
                rx.text(f"Host: {room.host_name}", color=colors["text_secondary"], font_size="0.85rem"),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text(
                    f"{room.current_participants}/{room.max_participants}",
                    color=colors["accent_gold"],
                    font_family="'Press Start 2P', monospace",
                    font_size="10px",
                ),
                rx.text("players", color=colors["text_secondary"], font_size="0.7rem"),
                align_items="center",
            ),
            width="100%",
            align_items="center",
        ),
        rx.cond(
            ~is_full,
            game_button(
                "🚪 GÕ CỬA",
                on_click=RoomState.request_join(room.id),
                variant="primary",
            ),
            rx.text("PHÒNG ĐẦY", color=colors["danger"], font_family="'Press Start 2P', monospace", font_size="10px"),
        ),
        width="100%",
    )
```

#### `forfriend/components/chat/message_bubble.py`

```python
import reflex as rx
from ...styles.theme import colors

def message_bubble(message) -> rx.Component:
    """RPG-style dialog box cho tin nhắn."""
    bubble_style = {
        "background": colors["accent_primary"] if message.is_mine else colors["bg_card"],
        "color": colors["bg_primary"] if message.is_mine else colors["text_primary"],
        "padding": "10px 14px",
        "border_radius": "8px",
        "max_width": "70%",
        "border": f"2px solid {colors['accent_primary'] if message.is_mine else colors['border']}",
        "position": "relative",
    }
    return rx.box(
        rx.text(message.content, style={"font_size": "0.9rem"}),
        rx.text(
            message.created_at,
            style={"font_size": "0.65rem", "color": colors["text_secondary"], "margin_top": "4px"},
        ),
        style=bubble_style,
        align_self="flex-end" if message.is_mine else "flex-start",
    )
```

---

### 11.4. Pages (Python thuần)

#### `forfriend/pages/login.py`

```python
import reflex as rx
from ..state.auth_state import AuthState
from ..components.common import game_button, game_input, pixel_title
from ..styles.theme import colors

def login_page() -> rx.Component:
    return rx.box(
        # Animated background
        rx.box(
            style={
                "position": "fixed", "inset": "0",
                "background": f"radial-gradient(ellipse at center, {colors['bg_secondary']} 0%, {colors['bg_primary']} 100%)",
                "z_index": "-1",
            }
        ),
        rx.center(
            rx.vstack(
                # Logo
                rx.image(src="/assets/logo.png", width="80px", class_name="float"),
                pixel_title("STUDY BUDDY", size="1.5rem"),
                rx.text("FIND YOUR PARTY", color=colors["text_secondary"], font_size="0.7rem",
                        font_family="'Press Start 2P', monospace"),

                # Form
                rx.vstack(
                    game_input("Email", AuthState.email if hasattr(AuthState, "email") else "",
                               AuthState.set_email if hasattr(AuthState, "set_email") else lambda x: x),
                    game_input("Password", "", lambda x: x, input_type="password"),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.text(AuthState.error_message, color=colors["danger"], font_size="0.8rem"),
                    ),
                    game_button(
                        rx.cond(AuthState.is_loading, "LOADING...", "▶ START GAME"),
                        on_click=AuthState.login({}),
                    ),
                    rx.link(
                        "NEW PLAYER? REGISTER →",
                        href="/register",
                        style={"color": colors["text_secondary"], "font_size": "0.65rem",
                               "font_family": "'Press Start 2P', monospace",
                               "_hover": {"color": colors["accent_primary"]}},
                    ),
                    spacing="4",
                    width="300px",
                ),
                spacing="6",
                align_items="center",
            ),
            height="100vh",
        ),
    )
```

#### `forfriend/pages/feed.py`

```python
import reflex as rx
from ..state.feed_state import FeedState
from ..components.feed.post_card import post_card
from ..components.common import game_button, pixel_title
from ..styles.theme import colors

def feed_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                pixel_title("📋 QUEST BOARD"),
                rx.spacer(),
                game_button("+ POST QUEST", on_click=FeedState.set_show_create_modal(True)),
                width="100%",
                align_items="center",
            ),

            # Filter bar
            rx.hstack(
                *[
                    rx.button(
                        tag,
                        on_click=FeedState.set_filter_tag(tag),
                        style={
                            "background": rx.cond(
                                FeedState.filter_tag == tag,
                                colors["accent_primary"],
                                colors["bg_card"],
                            ),
                            "color": rx.cond(
                                FeedState.filter_tag == tag,
                                colors["bg_primary"],
                                colors["text_primary"],
                            ),
                            "border": f"1px solid {colors['border']}",
                            "padding": "4px 12px",
                            "border_radius": "16px",
                            "font_size": "0.8rem",
                        },
                    )
                    for tag in ["Tất cả", "Toán", "Lý", "Hóa", "Văn", "Anh"]
                ],
                spacing="2",
                flex_wrap="wrap",
            ),

            # Posts list
            rx.cond(
                FeedState.is_loading,
                rx.center(rx.spinner(color=colors["accent_primary"])),
                rx.vstack(
                    rx.foreach(FeedState.posts, post_card),
                    spacing="4",
                    width="100%",
                ),
            ),

            spacing="6",
            width="100%",
            padding="24px",
        ),
        on_mount=FeedState.load_feed,
    )
```

#### `forfriend/pages/video_call.py`

```python
import reflex as rx
from ..state.room_state import RoomState
from ..components.video.livekit_component import LiveKitRoom, VideoConference, RoomAudioRenderer
from ..components.video.control_bar import control_bar
from ..components.video.participant_list import participant_list
from ..styles.theme import colors

def video_call_page() -> rx.Component:
    """
    Video Call Room — LiveKit là ngoại lệ duy nhất dùng JS.
    Toàn bộ logic xung quanh (state, UI controls) là Python thuần.
    """
    return rx.box(
        rx.cond(
            RoomState.is_in_call,
            rx.hstack(
                # Main video area — LiveKit JS Component
                rx.box(
                    LiveKitRoom(
                        server_url=RoomState.livekit_url,
                        token=RoomState.livekit_token,
                        children=[
                            VideoConference(),
                            RoomAudioRenderer(),
                        ],
                    ),
                    flex="1",
                    height="100vh",
                ),
                # Sidebar — Python thuần
                rx.box(
                    participant_list(),
                    width="280px",
                    height="100vh",
                    background=colors["bg_secondary"],
                    border_left=f"1px solid {colors['border']}",
                ),
                width="100%",
            ),
            # Chưa có token — đang chờ approve
            rx.center(
                rx.vstack(
                    rx.spinner(color=colors["accent_primary"], size="3"),
                    rx.text("Đang chờ host duyệt...",
                            color=colors["text_secondary"],
                            font_family="'Press Start 2P', monospace",
                            font_size="10px"),
                    spacing="4",
                ),
                height="100vh",
            ),
        ),
        # Control bar luôn hiển thị nếu đang trong phòng
        rx.cond(
            RoomState.is_in_call,
            control_bar(),
        ),
    )
```

---

### 11.5. Layout & Routing

#### `forfriend/components/layout/game_layout.py`

```python
import reflex as rx
from ...state.auth_state import AuthState
from ...styles.theme import colors
from ..common import avatar_display

def game_sidebar() -> rx.Component:
    """Navigation sidebar — pixel art style."""
    nav_items = [
        ("🏠", "HOME", "/"),
        ("📋", "FEED", "/feed"),
        ("🎮", "ROOMS", "/rooms"),
        ("💬", "CHAT", "/friends"),
        ("👤", "PROFILE", "/profile"),
    ]
    return rx.box(
        rx.vstack(
            # Logo
            rx.text("SB", style={
                "font_family": "'Press Start 2P', monospace",
                "font_size": "1.5rem",
                "color": colors["accent_primary"],
                "text_shadow": f"0 0 10px {colors['accent_primary']}",
                "padding": "16px",
            }),
            rx.divider(border_color=colors["border"]),
            # Nav items
            *[
                rx.link(
                    rx.hstack(
                        rx.text(icon, font_size="1.2rem"),
                        rx.text(label, font_family="'Press Start 2P', monospace", font_size="8px"),
                        spacing="3",
                        padding="12px 16px",
                    ),
                    href=href,
                    style={
                        "color": colors["text_secondary"],
                        "text_decoration": "none",
                        "width": "100%",
                        "_hover": {
                            "color": colors["accent_primary"],
                            "background": colors["bg_card"],
                        },
                    },
                )
                for icon, label, href in nav_items
            ],
            rx.spacer(),
            # User info
            rx.hstack(
                avatar_display(AuthState.user_avatar_id, size="32px"),
                rx.text(AuthState.user_name, font_size="0.75rem", color=colors["text_secondary"]),
                padding="16px",
            ),
            height="100vh",
            width="200px",
            spacing="0",
        ),
        background=colors["bg_secondary"],
        border_right=f"1px solid {colors['border']}",
    )


def game_layout(*page_content) -> rx.Component:
    """Main layout wrapper với sidebar."""
    return rx.hstack(
        game_sidebar(),
        rx.box(
            *page_content,
            flex="1",
            overflow="auto",
            height="100vh",
        ),
        spacing="0",
        width="100%",
    )
```

#### `forfriend/forfriend.py` — App entry + routes

```python
import reflex as rx
from .pages import login, register, dashboard, feed, rooms, video_call, chat, profile
from .components.layout.game_layout import game_layout

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;500;600;700&display=swap",
        "styles/global.css",
    ],
    style={"background": "#0a0a1a", "min_height": "100vh"},
)

# Public routes
app.add_page(login.login_page, route="/login")
app.add_page(register.register_page, route="/register")

# Protected routes (wrapped với game_layout)
def protected(page_fn):
    def wrapper():
        return game_layout(page_fn())
    return wrapper

app.add_page(protected(dashboard.dashboard_page), route="/")
app.add_page(protected(feed.feed_page), route="/feed")
app.add_page(protected(rooms.rooms_page), route="/rooms")
app.add_page(protected(chat.chat_page), route="/chat/[friend_id]")
app.add_page(protected(profile.profile_page), route="/profile")
app.add_page(video_call.video_call_page, route="/rooms/[room_id]/call")  # Fullscreen
```

---

### 11.6. Avatar Selector (Multi-step Register)

```python
# forfriend/components/user/avatar_selector.py
import reflex as rx
from ...state.register_state import RegisterState
from ...styles.theme import colors

def avatar_selector() -> rx.Component:
    """Grid 15 avatar chibi để chọn khi đăng ký."""
    return rx.vstack(
        rx.text("CHOOSE YOUR HERO", font_family="'Press Start 2P', monospace",
                color=colors["accent_primary"], font_size="0.9rem"),
        rx.grid(
            rx.foreach(
                rx.Var.range(1, 16),  # 1..15
                lambda i: rx.box(
                    rx.image(
                        src=f"/assets/avatars/avatar-{i:02d}.png",
                        width="64px", height="64px",
                        style={"image_rendering": "pixelated"},
                    ),
                    on_click=RegisterState.set_avatar_id(i),
                    style={
                        "border": rx.cond(
                            RegisterState.avatar_id == i,
                            f"3px solid {colors['accent_primary']}",
                            f"3px solid {colors['border']}",
                        ),
                        "border_radius": "8px",
                        "padding": "4px",
                        "cursor": "pointer",
                        "box_shadow": rx.cond(
                            RegisterState.avatar_id == i,
                            f"0 0 12px {colors['accent_primary']}",
                            "none",
                        ),
                        "_hover": {"border_color": colors["accent_primary"]},
                    },
                ),
            ),
            columns="5",
            spacing="3",
        ),
        spacing="4",
    )
```

---

### 11.7. Cấu trúc thư mục hoàn chỉnh

```
frontend/
├── forfriend/
│   ├── __init__.py
│   ├── forfriend.py               # App entry + routing
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   ├── register.py             # Multi-step form
│   │   ├── dashboard.py
│   │   ├── feed.py
│   │   ├── rooms.py
│   │   ├── video_call.py           # LiveKit integration
│   │   ├── chat.py
│   │   └── profile.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── common.py               # game_button, game_card, game_input, pixel_title...
│   │   ├── layout/
│   │   │   ├── game_layout.py      # Sidebar + main area
│   │   │   └── top_bar.py
│   │   ├── user/
│   │   │   ├── avatar_display.py
│   │   │   └── avatar_selector.py  # Grid 15 avatar
│   │   ├── feed/
│   │   │   ├── post_card.py
│   │   │   └── create_post_modal.py
│   │   ├── room/
│   │   │   ├── category_zone.py
│   │   │   ├── room_card.py
│   │   │   └── pending_requests.py
│   │   ├── video/
│   │   │   ├── livekit_component.py   # ⚠️ JS bridge (ngoại lệ duy nhất)
│   │   │   ├── control_bar.py         # Python thuần
│   │   │   └── participant_list.py    # Python thuần
│   │   ├── chat/
│   │   │   ├── message_bubble.py
│   │   │   ├── chat_input.py
│   │   │   └── typing_indicator.py
│   │   └── rating/
│   │       └── rating_modal.py
│   ├── state/
│   │   ├── __init__.py
│   │   ├── auth_state.py            # Login, logout, token
│   │   ├── register_state.py        # Multi-step register
│   │   ├── feed_state.py            # Feed + create post
│   │   ├── room_state.py            # Rooms + LiveKit token
│   │   ├── chat_state.py            # Messages
│   │   └── notification_state.py    # Toast + WebSocket events
│   ├── styles/
│   │   ├── theme.py                 # CSS variables as Python dict
│   │   └── global.css               # Keyframe animations
│   └── assets/
│       ├── avatars/                 # 15 avatar chibi PNG
│       ├── sounds/                  # join.mp3, leave.mp3...
│       └── logo.png
├── rxconfig.py
└── requirements.txt
```

> **Quan trọng**: Dùng tool `generate_image` để tạo 15 avatar chibi theo phong cách pixel art / anime chibi. Mỗi avatar nên có personality riêng (khác tóc, màu, trang phục).

---

### 11.8. Responsive Design

Reflex dùng Chakra UI breakpoints:

```python
# Ví dụ responsive trong Reflex
rx.box(
    ...,
    width=rx.breakpoints(sm="100%", md="50%", lg="33%"),
    display=rx.breakpoints(base="none", md="block"),  # Hide trên mobile
)
```

- **Desktop** (≥1024px): Full layout, sidebar mở
- **Tablet** (768–1023px): Sidebar collapsed, grid 2 cột
- **Mobile** (<768px): Bottom navigation, stack 1 cột

---

## Tiêu chí hoàn thành

- [ ] Design system (`theme.py` + `global.css`) hoàn chỉnh
- [ ] Tất cả State classes hoạt động (AuthState, FeedState, RoomState, ChatState)
- [ ] Tất cả pages render đúng, routing hoạt động
- [ ] Login/Register flow hoàn chỉnh (multi-step register + avatar selector)
- [ ] Feed hiển thị posts + filter + tạo bài mới
- [ ] Room lobby: categories grid + room list + request join
- [ ] Video call: LiveKit Custom Component hoạt động + control bar Python
- [ ] Chat: message bubbles + gửi tin nhắn
- [ ] Rating modal hiện sau khi rời phòng
- [ ] 15 avatar chibi assets có sẵn trong `/assets/avatars/`
- [ ] Responsive (desktop + tablet + mobile) qua Reflex breakpoints
- [ ] Animations mượt (hover, transitions, micro-interactions qua CSS)
- [ ] Giao diện đúng phong cách game retro (pixel font, neon colors, glow effects)
- [ ] `reflex run` không lỗi, không warning Python
- [ ] JS duy nhất là `livekit_component.py` (~30 dòng)
