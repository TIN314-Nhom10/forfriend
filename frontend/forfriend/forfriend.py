"""Entry Point chính của Reflex App ForFriend: Cấu hình App & Đăng ký Routes."""
import reflex as rx
from .styles.theme import GLOBAL_STYLES
from .pages import (
    login_page,
    register_page,
    dashboard_page,
    feed_page,
    rooms_page,
    video_call_page,
    friends_page,
    profile_page,
)

from .state.room_state import RoomState

app = rx.App(
    style=GLOBAL_STYLES,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Press+Start+2P&family=Inter:wght@400;500;600;700&display=swap",
        "/styles/global.css",
    ],
)

# Đăng ký các Routes của ứng dụng ForFriend
app.add_page(
    dashboard_page,
    route="/",
    title="ForFriend — Student Study Hub",
)
app.add_page(
    login_page,
    route="/login",
    title="ForFriend — Login",
)
app.add_page(
    register_page,
    route="/register",
    title="ForFriend — Create Account",
)
app.add_page(
    feed_page,
    route="/feed",
    title="ForFriend — Study Partner Feed",
)
app.add_page(
    rooms_page,
    route="/rooms",
    title="ForFriend — Study Rooms Lobby",
)
app.add_page(
    video_call_page,
    route="/rooms/[room_id]",
    title="ForFriend — Virtual Study Room",
    on_load=RoomState.on_video_call_mount,
)
app.add_page(
    friends_page,
    route="/friends",
    title="ForFriend — Friends & Chat",
)
app.add_page(
    profile_page,
    route="/profile",
    title="ForFriend — Profile & Student Verification",
)
