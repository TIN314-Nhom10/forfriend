"""Friends & Chat Page: Quán trọ Bạn bè & Nhắn tin thời gian thực 1-1 với Glassmorphism."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.common import pixel_title, avatar_display, status_badge
from ..components.layout.game_layout import game_layout
from ..components.chat.chat_components import friend_item, friend_request_item, message_bubble, chat_input_bar
from ..state.chat_state import ChatState
from ..state.base_state import BaseState


def friends_page() -> rx.Component:
    """Giao diện quản lý bạn bè và chat 1-1 phong cách Cyber Glass."""
    return game_layout(
        rx.box(
            rx.hstack(
                # Left Panel: Friends & Requests List
                rx.box(
                    rx.vstack(
                        pixel_title(
                            "💬 ALLIES & CHAT",
                            size="18px",
                            color=COLORS["neon_pink"],
                        ),
                        # Friend Requests Section (if any)
                        rx.cond(
                            ChatState.friend_requests.length() > 0,
                            rx.vstack(
                                rx.text(
                                    f"Friend Requests ({ChatState.friend_requests.length()}):",
                                    font_family=FONTS["ui"],
                                    font_size="12px",
                                    font_weight="700",
                                    color=COLORS["neon_gold"],
                                ),
                                rx.foreach(ChatState.friend_requests, friend_request_item),
                                spacing="2",
                                width="100%",
                                margin_bottom="12px",
                            ),
                        ),
                        # Friends List
                        rx.text(
                            "Study Allies List:",
                            font_family=FONTS["ui"],
                            font_size="12px",
                            font_weight="700",
                            color=COLORS["neon_green"],
                        ),
                        rx.cond(
                            ChatState.friends.length() == 0,
                            rx.text(
                                "No allies yet. Check Quest Board to make friends!",
                                font_size="13px",
                                color=COLORS["text_muted"],
                            ),
                            rx.vstack(
                                rx.foreach(ChatState.friends, friend_item),
                                spacing="2",
                                width="100%",
                            ),
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    width=["100%", "290px"],
                    background_color="rgba(18, 18, 38, 0.75)",
                    backdrop_filter="blur(16px)",
                    padding="18px",
                    border_radius="12px",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                    box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.36)",
                    height="calc(100vh - 64px)",
                    overflow_y="auto",
                ),
                # Right Panel: Active Conversation Window
                rx.box(
                    rx.cond(
                        ChatState.active_friend_id != "",
                        rx.vstack(
                            # Chat Top Bar
                            rx.hstack(
                                avatar_display(ChatState.active_friend_avatar, size="42px", border_glow=ChatState.active_friend_online),
                                rx.vstack(
                                    rx.text(ChatState.active_friend_name, font_family=FONTS["ui"], font_weight="700", color=COLORS["text_main"], font_size="16px"),
                                    status_badge(ChatState.active_friend_online, None),
                                    spacing="1",
                                    align="start",
                                ),
                                rx.spacer(),
                                rx.button(
                                    "Remove Ally",
                                    on_click=ChatState.remove_friend(ChatState.active_friend_id),
                                    font_family=FONTS["ui"],
                                    font_size="12px",
                                    font_weight="600",
                                    background="rgba(255, 77, 109, 0.08)",
                                    color=COLORS["danger"],
                                    border=f"1px solid rgba(255, 77, 109, 0.25)",
                                    border_radius="6px",
                                    padding="6px 12px",
                                    cursor="pointer",
                                    transition="all 150ms ease",
                                    _hover={"background": "rgba(255, 77, 109, 0.2)", "border_color": COLORS["danger"]},
                                ),
                                padding="14px 18px",
                                border_bottom="1px solid rgba(255, 255, 255, 0.06)",
                                width="100%",
                                align="center",
                            ),
                            # Messages Scroll Area
                            rx.box(
                                rx.cond(
                                    ChatState.messages.length() == 0,
                                    rx.center(
                                        rx.vstack(
                                            rx.text("📜", font_size="36px"),
                                            rx.text(
                                                "Start conversation with your ally!",
                                                font_family=FONTS["ui"],
                                                font_size="14px",
                                                font_weight="600",
                                                color=COLORS["text_muted"],
                                            ),
                                            spacing="2",
                                            align="center",
                                        ),
                                        height="100%",
                                    ),
                                    rx.vstack(
                                        rx.foreach(ChatState.messages, message_bubble),
                                        spacing="1",
                                        width="100%",
                                    ),
                                ),
                                flex="1",
                                width="100%",
                                overflow_y="auto",
                                padding="18px",
                            ),
                            # Chat Input Bar
                            chat_input_bar(),
                            height="100%",
                            width="100%",
                            spacing="0",
                        ),
                        # Empty state when no friend selected
                        rx.center(
                            rx.vstack(
                                rx.box(
                                    rx.text("💬", font_size="44px", color=COLORS["neon_green"]),
                                    padding="20px",
                                    border_radius="50%",
                                    background="rgba(0, 255, 136, 0.06)",
                                    border="1px solid rgba(0, 255, 136, 0.2)",
                                ),
                                pixel_title(
                                    "SELECT AN ALLY TO CHAT",
                                    size="16px",
                                    color=COLORS["neon_green"],
                                ),
                                rx.text(
                                    "Click on an ally in the left list to start real-time 1-on-1 chat.",
                                    font_family=FONTS["ui"],
                                    font_size="14px",
                                    color=COLORS["text_muted"],
                                ),
                                spacing="3",
                                align="center",
                            ),
                            height="100%",
                            width="100%",
                        ),
                    ),
                    flex="1",
                    background_color="rgba(18, 18, 38, 0.75)",
                    backdrop_filter="blur(16px)",
                    padding="18px",
                    border_radius="12px",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                    box_shadow="0 8px 32px 0 rgba(0, 0, 0, 0.36)",
                    height="calc(100vh - 64px)",
                    display="flex",
                    flex_direction="column",
                ),
                spacing="4",
                align="start",
                width="100%",
            ),
            width="100%",
        ),
        on_mount=ChatState.load_chat_page,
    )
