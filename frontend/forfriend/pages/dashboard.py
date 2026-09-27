"""Dashboard Page: Giao diện chuẩn theo thiết kế tham chiếu ForFriend."""
import reflex as rx
from .feed import feed_page


def dashboard_page() -> rx.Component:
    """Dashboard đồng bộ với mockup thiết kế tham chiếu ForFriend."""
    return feed_page()
