"""Export toàn bộ Reflex pages."""
from .login import login_page
from .register import register_page
from .dashboard import dashboard_page
from .feed import feed_page
from .rooms import rooms_page
from .video_call import video_call_page
from .friends import friends_page
from .profile import profile_page

__all__ = [
    "login_page",
    "register_page",
    "dashboard_page",
    "feed_page",
    "rooms_page",
    "video_call_page",
    "friends_page",
    "profile_page",
]
