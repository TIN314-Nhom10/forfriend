"""Quest Card Component: Thẻ bài đăng tìm bạn học phong cách Modern Game Quest & Glassmorphism."""
import reflex as rx
from ...styles.theme import COLORS, FONTS, btn_primary_style, btn_secondary_style, game_card_style
from ..common import avatar_display
from ...state.base_state import BaseState
from ...state.feed_state import FeedState
from ...state.chat_state import ChatState
from ...state.models import PostItem


def tag_pill(tag: str) -> rx.Component:
    """Huy hiệu tag môn học dạng slate pill tinh tế."""
    return rx.badge(
        tag,
        bg="#182c36",
        color="#cbd5e1",
        border="1px solid rgba(255, 255, 255, 0.08)",
        font_family=FONTS["ui"],
        font_size="11px",
        font_weight="600",
        padding="3px 10px",
        border_radius="6px",
    )


def quest_card(post: PostItem) -> rx.Component:
    """Card hiển thị 1 Quest tìm bạn học chuẩn giao diện tham chiếu ForFriend."""
    return rx.box(
        rx.vstack(
            # Top Header Row: "Study Quest" + Options "•••"
            rx.hstack(
                rx.text(
                    "Study Quest",
                    font_family=FONTS["ui"],
                    font_size="13px",
                    font_weight="700",
                    color=COLORS["neon_green"],
                ),
                rx.spacer(),
                rx.box(
                    rx.text(
                        "•••",
                        font_size="16px",
                        color=COLORS["text_muted"],
                        cursor="pointer",
                        _hover={"color": COLORS["text_main"]},
                    ),
                    on_click=FeedState.share_quest(post.title),
                ),
                width="100%",
                align="center",
            ),
            # Quest Title
            rx.heading(
                post.title,
                font_family=FONTS["heading"],
                font_size="18px",
                font_weight="700",
                color=COLORS["text_main"],
                line_height="1.3",
                margin_top="4px",
            ),
            # Author Row with Chibi Avatar
            rx.hstack(
                avatar_display(post.author_avatar_id, size="42px", border_glow=False),
                rx.vstack(
                    rx.text(
                        post.author_name,
                        font_family=FONTS["ui"],
                        font_size="14px",
                        font_weight="700",
                        color=COLORS["text_main"],
                    ),
                    rx.hstack(
                        rx.text(
                            "Uni: " + post.author_school,
                            font_family=FONTS["ui"],
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        rx.text(
                            post.author_rating.to_string() + "★",
                            font_family=FONTS["ui"],
                            font_size="12px",
                            font_weight="700",
                            color=COLORS["neon_gold"],
                        ),
                        spacing="1",
                        align="center",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                margin_top="8px",
                width="100%",
            ),
            # Content Description
            rx.text(
                post.content,
                font_family=FONTS["body"],
                font_size="13px",
                color="#8fa0ad",
                line_height="1.5",
                margin_top="8px",
            ),
            # Tags Row
            rx.hstack(
                rx.foreach(post.tags, tag_pill),
                spacing="2",
                wrap="wrap",
                margin_top="10px",
                width="100%",
            ),
            # Teammates stack + rating
            rx.hstack(
                rx.hstack(
                    avatar_display("1", size="22px", border_glow=False),
                    avatar_display("2", size="22px", border_glow=False, margin_left="-8px"),
                    avatar_display("3", size="22px", border_glow=False, margin_left="-8px"),
                    spacing="0",
                ),
                rx.text(
                    post.author_rating.to_string() + "★",
                    font_family=FONTS["ui"],
                    font_size="11px",
                    font_weight="700",
                    color=COLORS["neon_gold"],
                    margin_left="6px",
                ),
                spacing="1",
                align="center",
                margin_top="10px",
                width="100%",
            ),
            # Action Buttons Row
            rx.hstack(
                rx.button(
                    "View Details",
                    on_click=FeedState.view_quest_details(post),
                    style=btn_secondary_style,
                    flex="1",
                ),
                rx.cond(
                    post.is_mine,
                    rx.button(
                        "🗑 Delete",
                        on_click=FeedState.delete_quest(post.id),
                        font_family=FONTS["ui"],
                        font_size="13px",
                        font_weight="600",
                        background="rgba(244, 63, 94, 0.12)",
                        color=COLORS["danger"],
                        border="1px solid rgba(244, 63, 94, 0.3)",
                        border_radius="8px",
                        padding="9px 16px",
                        cursor="pointer",
                        flex="1",
                        _hover={"background": "rgba(244, 63, 94, 0.22)"},
                    ),
                    rx.button(
                        "Request Join",
                        on_click=ChatState.send_friend_request(post.author_id),
                        style=btn_primary_style,
                        flex="1",
                    ),
                ),
                spacing="3",
                width="100%",
                margin_top="14px",
            ),
            spacing="1",
            width="100%",
        ),
        style=game_card_style,
        width="100%",
    )

