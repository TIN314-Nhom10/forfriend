"""Feed Page: Bảng tin Quest tìm bạn học phong cách Neo-Cyber Student & Glassmorphism."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.layout.game_layout import game_layout
from ..components.layout.top_header import top_header
from ..components.layout.right_sidebar import right_sidebar
from ..components.feed.quest_card import quest_card
from ..components.feed.filter_bar import filter_bar
from ..components.feed.create_quest_modal import create_quest_modal
from ..components.common import avatar_display
from ..state.feed_state import FeedState
from ..state.base_state import BaseState
from ..state.chat_state import ChatState


def quest_details_modal() -> rx.Component:
    """Modal hiển thị chi tiết Study Quest."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.badge("Study Quest", bg="#182c36", color=COLORS["neon_green"], border_radius="6px", padding="4px 10px"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button("✕", variant="ghost", color=COLORS["text_muted"], cursor="pointer", on_click=FeedState.close_quest_details),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.heading(
                    FeedState.details_title,
                    font_family=FONTS["heading"],
                    font_size="20px",
                    font_weight="700",
                    color=COLORS["text_main"],
                    margin_top="8px",
                ),
                rx.hstack(
                    avatar_display(FeedState.details_author_avatar, size="48px", border_glow=False),
                    rx.vstack(
                        rx.text(FeedState.details_author_name, font_family=FONTS["ui"], font_size="15px", font_weight="700", color=COLORS["text_main"]),
                        rx.hstack(
                            rx.text("Uni: " + FeedState.details_author_school, font_size="13px", color=COLORS["text_muted"]),
                            rx.text(FeedState.details_author_rating.to_string() + "★", font_size="13px", font_weight="700", color=COLORS["neon_gold"]),
                            spacing="2",
                            align="center",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                    margin_top="12px",
                ),
                rx.box(
                    rx.text(
                        FeedState.details_content,
                        font_family=FONTS["body"],
                        font_size="14px",
                        color="#cbd5e1",
                        line_height="1.6",
                    ),
                    padding="16px",
                    border_radius="10px",
                    background="rgba(255, 255, 255, 0.03)",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                    margin_top="14px",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("📍 Location / Study Mode: ", font_size="13px", color=COLORS["text_muted"], font_weight="600"),
                    rx.text(
                        rx.cond(FeedState.details_is_online, "Online Discord / LiveKit", FeedState.details_location),
                        font_size="13px",
                        color=COLORS["neon_green"],
                        font_weight="700",
                    ),
                    spacing="2",
                    align="center",
                    margin_top="10px",
                ),
                rx.hstack(
                    rx.button(
                        "Close",
                        on_click=FeedState.close_quest_details,
                        variant="ghost",
                        flex="1",
                        border="1px solid rgba(255, 255, 255, 0.15)",
                    ),
                    rx.button(
                        "Request Join / Chat",
                        on_click=ChatState.send_friend_request(FeedState.details_author_id),
                        background_color=COLORS["neon_green"],
                        color="#0b1319",
                        font_weight="700",
                        flex="1",
                    ),
                    spacing="3",
                    width="100%",
                    margin_top="18px",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            background_color="#13222a",
            border="1px solid rgba(44, 234, 163, 0.3)",
            border_radius="16px",
            padding="24px",
            max_width="520px",
            width="90vw",
        ),
        open=FeedState.show_details_modal,
        on_open_change=lambda _: FeedState.close_quest_details(),
    )


def feed_page() -> rx.Component:
    """Giao diện Bảng tin Quest chuẩn theo thiết kế tham chiếu ForFriend."""
    return game_layout(
        rx.box(
            create_quest_modal(),
            quest_details_modal(),
            # Top Search & User Header
            top_header(),
            # Main Content Layout: Center 2-Column Feed + Right Profile Sidebar
            rx.hstack(
                # Left/Center Feed Column
                rx.vstack(
                    filter_bar(),
                    # Quest Cards 2-Column Grid
                    rx.cond(
                        FeedState.is_loading,
                        rx.center(
                            rx.vstack(
                                rx.spinner(color=COLORS["neon_green"], size="3"),
                                rx.text(
                                    "Loading Study Quests...",
                                    font_family=FONTS["ui"],
                                    font_size="14px",
                                    font_weight="600",
                                    color=COLORS["neon_green"],
                                ),
                                spacing="3",
                            ),
                            height="300px",
                            width="100%",
                        ),
                        rx.cond(
                            FeedState.posts.length() == 0,
                            rx.center(
                                rx.vstack(
                                    rx.box(
                                        rx.text("⚡", font_size="36px", color=COLORS["neon_green"]),
                                        padding="16px",
                                        border_radius="50%",
                                        background="rgba(44, 234, 163, 0.08)",
                                        border="1px solid rgba(44, 234, 163, 0.2)",
                                    ),
                                    rx.text(
                                        "No study quests found matching current filter.",
                                        font_family=FONTS["ui"],
                                        font_size="15px",
                                        font_weight="600",
                                        color=COLORS["text_muted"],
                                    ),
                                    rx.button(
                                        "Post First Quest",
                                        on_click=FeedState.toggle_create_modal,
                                        background_color=COLORS["neon_green"],
                                        color="#0b1319",
                                        font_weight="700",
                                        border_radius="8px",
                                        padding="8px 20px",
                                    ),
                                    spacing="3",
                                    align="center",
                                ),
                                height="280px",
                                width="100%",
                            ),
                            rx.grid(
                                rx.foreach(FeedState.posts, quest_card),
                                columns={"initial": "1", "sm": "1", "md": "2"},
                                spacing="4",
                                width="100%",
                            ),
                        ),
                    ),
                    spacing="0",
                    flex="1",
                    width="100%",
                ),
                # Right Sidebar (Welcome Liam M., Active Quests, Recent Contacts)
                right_sidebar(),
                spacing="4",
                align="start",
                width="100%",
            ),
            width="100%",
        ),
        on_mount=FeedState.load_feed,
    )

