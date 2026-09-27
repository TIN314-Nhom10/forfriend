"""Top Header Component: Search Bar, Notifications và User Profile pill theo chuẩn mockup."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import avatar_display
from ...state.base_state import BaseState
from ...state.feed_state import FeedState


def top_header() -> rx.Component:
    """Header trên cùng chứa thanh tìm kiếm, chuông thông báo và user pill."""
    return rx.hstack(
        # Search Box
        rx.hstack(
            rx.box(
                rx.text("🔍", font_size="14px", color=COLORS["text_muted"]),
                cursor="pointer",
                on_click=FeedState.load_feed,
            ),
            rx.input(
                placeholder="Search for partners, subjects, or quests...",
                value=FeedState.search_query,
                on_change=FeedState.set_search_query,
                on_blur=FeedState.load_feed,
                font_family=FONTS["ui"],
                font_size="13px",
                color=COLORS["text_main"],
                background_color="transparent",
                border="none",
                width="100%",
                _focus={"outline": "none"},
            ),
            spacing="2",
            align="center",
            padding="9px 16px",
            border_radius="9999px",
            background_color="rgba(19, 34, 42, 0.8)",
            border="1px solid rgba(255, 255, 255, 0.08)",
            width=["100%", "360px", "440px"],
            transition="all 200ms ease",
            _hover={"border_color": "rgba(44, 234, 163, 0.3)"},
            _focus_within={
                "border_color": COLORS["neon_green"],
                "box_shadow": f"0 0 14px {COLORS['neon_green']}33",
            },
        ),
        rx.spacer(),
        # Right Actions: Notification Bell + User Dropdown Pill
        rx.hstack(
            # Notification Bell Button
            rx.box(
                rx.text("🔔", font_size="16px", color=COLORS["text_muted"]),
                padding="8px 10px",
                border_radius="10px",
                background_color="rgba(19, 34, 42, 0.8)",
                border="1px solid rgba(255, 255, 255, 0.08)",
                cursor="pointer",
                _hover={"border_color": COLORS["neon_green"]},
            ),
            # User Pill
            rx.link(
                rx.hstack(
                    avatar_display(
                        rx.cond(BaseState.avatar_id != "", BaseState.avatar_id, "1"),
                        size="30px",
                        border_glow=False,
                    ),
                    rx.text(
                        rx.cond(
                            BaseState.is_authenticated,
                            BaseState.user_name,
                            "Liam M.",
                        ),
                        font_family=FONTS["ui"],
                        font_size="13px",
                        font_weight="700",
                        color=COLORS["text_main"],
                        max_width="100px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                    ),
                    rx.text("▼", font_size="9px", color=COLORS["text_muted"]),
                    spacing="2",
                    align="center",
                    padding="4px 12px 4px 6px",
                    border_radius="9999px",
                    background_color="rgba(19, 34, 42, 0.8)",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                    cursor="pointer",
                    _hover={"border_color": COLORS["neon_green"]},
                ),
                href="/profile",
                text_decoration="none",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        align="center",
        padding_y="12px",
        margin_bottom="12px",
    )
