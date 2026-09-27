"""Chat UI Components: Danh sách bạn bè, hộp thoại RPG, và thanh nhập tin nhắn với Glassmorphism."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import avatar_display, status_badge, game_button
from ...state.chat_state import ChatState
from ...state.base_state import BaseState
from ...state.models import FriendItem, FriendRequestItem, MessageItem


def friend_item(friend: FriendItem) -> rx.Component:
    """Từng bạn bè trong danh sách với hiệu ứng glass hover."""
    is_active = ChatState.active_friend_id == friend.user_id

    return rx.box(
        rx.hstack(
            avatar_display(friend.avatar_id, size="40px", border_glow=friend.is_online),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        friend.name,
                        font_family=FONTS["ui"],
                        font_weight="700",
                        color=COLORS["text_main"],
                        font_size="14px",
                    ),
                    rx.spacer(),
                    status_badge(friend.is_online, ""),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    friend.school,
                    font_family=FONTS["ui"],
                    font_size="12px",
                    color=COLORS["text_muted"],
                    max_width="140px",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),
                spacing="1",
                align="start",
                width="100%",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        on_click=ChatState.select_friend(
            friend.user_id,
            friend.name,
            friend.avatar_id,
            friend.is_online,
        ),
        padding="10px 12px",
        border_radius="10px",
        cursor="pointer",
        background_color=rx.cond(is_active, "rgba(0, 255, 136, 0.12)", "transparent"),
        border=rx.cond(is_active, f"1px solid {COLORS['neon_green']}", "1px solid transparent"),
        box_shadow=rx.cond(is_active, "0 0 12px rgba(0, 255, 136, 0.2)", "none"),
        transition="all 150ms ease",
        _hover={"background_color": "rgba(255, 255, 255, 0.05)"},
        width="100%",
    )


def friend_request_item(req: FriendRequestItem) -> rx.Component:
    """Lời mời kết bạn đang chờ."""
    return rx.hstack(
        avatar_display(req.avatar_id, size="36px"),
        rx.vstack(
            rx.text(req.name, font_family=FONTS["ui"], font_weight="700", color=COLORS["text_main"], font_size="13px"),
            rx.text(req.school, font_family=FONTS["ui"], font_size="11px", color=COLORS["text_muted"]),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.button(
            "✓",
            on_click=ChatState.accept_request(req.friendship_id),
            bg=COLORS["neon_green"],
            color="#04120a",
            font_size="13px",
            font_weight="bold",
            padding="4px 10px",
            border_radius="6px",
            cursor="pointer",
            _hover={"filter": "brightness(1.1)"},
        ),
        rx.button(
            "✕",
            on_click=ChatState.reject_request(req.friendship_id),
            bg="rgba(255, 77, 109, 0.1)",
            color=COLORS["danger"],
            border=f"1px solid rgba(255, 77, 109, 0.3)",
            font_size="13px",
            font_weight="bold",
            padding="4px 10px",
            border_radius="6px",
            cursor="pointer",
            _hover={"bg": "rgba(255, 77, 109, 0.25)"},
        ),
        spacing="2",
        align="center",
        padding="10px",
        background_color="rgba(255, 255, 255, 0.03)",
        border="1px solid rgba(255, 255, 255, 0.06)",
        border_radius="8px",
        width="100%",
    )


def message_bubble(msg: MessageItem) -> rx.Component:
    """Hộp thoại tin nhắn phong cách Cyber Glass."""
    return rx.box(
        rx.box(
            rx.text(msg.content, font_family=FONTS["body"], font_size="14px", line_height="1.5"),
            rx.text(
                msg.created_at,
                font_family=FONTS["ui"],
                font_size="10px",
                color=rx.cond(msg.is_mine, "rgba(4, 18, 10, 0.7)", COLORS["text_muted"]),
                text_align="right",
                margin_top="4px",
            ),
            background=rx.cond(
                msg.is_mine,
                "linear-gradient(135deg, #00ff88 0%, #00cc6a 100%)",
                "rgba(28, 28, 58, 0.75)",
            ),
            color=rx.cond(msg.is_mine, "#04120a", COLORS["text_main"]),
            padding="10px 16px",
            border_radius=rx.cond(msg.is_mine, "14px 14px 2px 14px", "14px 14px 14px 2px"),
            border=rx.cond(msg.is_mine, "none", "1px solid rgba(255, 255, 255, 0.08)"),
            max_width="72%",
            box_shadow=rx.cond(msg.is_mine, "0 4px 15px rgba(0, 255, 136, 0.25)", "0 4px 15px rgba(0, 0, 0, 0.3)"),
        ),
        width="100%",
        display="flex",
        justify_content=rx.cond(msg.is_mine, "flex-end", "flex-start"),
        margin_y="4px",
    )


def chat_input_bar() -> rx.Component:
    """Khung nhập và gửi tin nhắn 1-1."""
    return rx.hstack(
        rx.input(
            placeholder="Type message to your ally... (Press Enter)",
            value=ChatState.message_input,
            on_change=ChatState.set_message_input,
            on_key_down=ChatState.handle_key_down,
            background_color="rgba(10, 10, 24, 0.8)",
            border="1px solid rgba(255, 255, 255, 0.1)",
            color=COLORS["text_main"],
            font_family=FONTS["ui"],
            font_size="14px",
            padding="12px 16px",
            border_radius="10px",
            flex="1",
            outline="none",
            _focus={"border_color": COLORS["neon_green"], "box_shadow": "0 0 0 3px rgba(0, 255, 136, 0.2)"},
        ),
        game_button(
            "Send",
            on_click=ChatState.send_message,
            variant="primary",
            style={"font_size": "13px", "padding": "11px 20px"},
        ),
        spacing="3",
        align="center",
        width="100%",
        padding_top="12px",
    )
