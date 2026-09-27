"""Create Quest Modal Component: Popup tạo bài đăng tìm bạn học mới chuẩn Neo-Cyber Student."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import game_input, game_button, pixel_title
from ...state.feed_state import FeedState
from ...state.base_state import BaseState


def create_quest_modal() -> rx.Component:
    """Dialog tạo Quest mới phong cách Neo-Cyber Glassmorphism."""
    return rx.cond(
        FeedState.show_create_modal,
        rx.center(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        pixel_title(
                            "+ CREATE NEW QUEST",
                            size="16px",
                            color=COLORS["neon_green"],
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕",
                            on_click=FeedState.toggle_create_modal,
                            background="transparent",
                            color=COLORS["text_muted"],
                            cursor="pointer",
                            font_size="16px",
                            _hover={"color": "#ffffff"},
                        ),
                        width="100%",
                        align="center",
                    ),
                    # Auth Banner nếu chưa đăng nhập
                    rx.cond(
                        ~BaseState.is_authenticated,
                        rx.box(
                            rx.hstack(
                                rx.text("⚡", font_size="18px"),
                                rx.vstack(
                                    rx.text(
                                        "You are in guest mode. Log in to post Quests:",
                                        font_family=FONTS["ui"],
                                        font_size="12px",
                                        font_weight="700",
                                        color=COLORS["warning"],
                                    ),
                                    rx.button(
                                        "⚡ 1-Click Demo Login (Nguyen Van A - FTU)",
                                        on_click=BaseState.login_as_demo,
                                        size="2",
                                        background=COLORS["neon_green"],
                                        color="#04120a",
                                        font_weight="700",
                                        font_family=FONTS["ui"],
                                        border_radius="8px",
                                        cursor="pointer",
                                        box_shadow=f"0 0 12px {COLORS['neon_green']}66",
                                        _hover={"filter": "brightness(1.1)"},
                                    ),
                                    spacing="1",
                                    align_items="start",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            padding="12px 14px",
                            background="rgba(245, 158, 11, 0.12)",
                            border="1px solid rgba(245, 158, 11, 0.35)",
                            border_radius="10px",
                            width="100%",
                        ),
                    ),
                    # Form Inputs
                    rx.vstack(
                        rx.text(
                            "Quest Title:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input(
                            "e.g., Finding partner for Python & FastAPI project...",
                            FeedState.new_title,
                            FeedState.set_new_title,
                        ),
                        rx.text(
                            "Detailed Content:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        rx.text_area(
                            placeholder="Study goals, free time schedule, subjects to review...",
                            value=FeedState.new_content,
                            on_change=FeedState.set_new_content,
                            background_color="rgba(11, 15, 25, 0.85)",
                            border="1px solid rgba(255, 255, 255, 0.12)",
                            border_radius="10px",
                            color=COLORS["text_main"],
                            font_family=FONTS["body"],
                            font_size="14px",
                            line_height="1.5",
                            padding="12px 14px",
                            min_height="110px",
                            width="100%",
                            outline="none",
                            _focus={"border_color": COLORS["neon_green"], "box_shadow": f"0 0 0 3px rgba(0, 245, 155, 0.2)"},
                        ),
                        rx.text(
                            "Subject Tags (comma separated):",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input(
                            "Python, FastAPI, Calculus",
                            FeedState.new_tags_input,
                            FeedState.set_new_tags_input,
                        ),
                        # Online / Offline Switch
                        rx.hstack(
                            rx.text(
                                "Format:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            rx.button(
                                "🌐 Online",
                                on_click=FeedState.set_new_is_online(True),
                                font_family=FONTS["ui"],
                                font_size="12px",
                                font_weight="700",
                                background_color=rx.cond(FeedState.new_is_online, COLORS["neon_green"], "rgba(255, 255, 255, 0.04)"),
                                color=rx.cond(FeedState.new_is_online, "#04120a", COLORS["text_muted"]),
                                padding="6px 14px",
                                border_radius="8px",
                                border=rx.cond(FeedState.new_is_online, f"1px solid {COLORS['neon_green']}", "1px solid rgba(255, 255, 255, 0.08)"),
                            ),
                            rx.button(
                                "📍 Offline",
                                on_click=FeedState.set_new_is_online(False),
                                font_family=FONTS["ui"],
                                font_size="12px",
                                font_weight="700",
                                background_color=rx.cond(~FeedState.new_is_online, COLORS["neon_pink"], "rgba(255, 255, 255, 0.04)"),
                                color=rx.cond(~FeedState.new_is_online, "#ffffff", COLORS["text_muted"]),
                                padding="6px 14px",
                                border_radius="8px",
                                border=rx.cond(~FeedState.new_is_online, f"1px solid {COLORS['neon_pink']}", "1px solid rgba(255, 255, 255, 0.08)"),
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        # Location Input if Offline
                        rx.cond(
                            ~FeedState.new_is_online,
                            rx.vstack(
                                rx.text(
                                    "Offline Meeting Place:",
                                    font_family=FONTS["ui"],
                                    font_size="13px",
                                    font_weight="700",
                                    color=COLORS["neon_pink"],
                                ),
                                game_input(
                                    "e.g., Campus Library, Coffee Shop...",
                                    FeedState.new_location,
                                    FeedState.set_new_location,
                                ),
                                spacing="1",
                                width="100%",
                            ),
                        ),
                        # Error Message
                        rx.cond(
                            FeedState.create_error != "",
                            rx.text(
                                FeedState.create_error,
                                color=COLORS["danger"],
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="bold",
                            ),
                        ),
                        # Action Buttons
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                "Cancel",
                                on_click=FeedState.toggle_create_modal,
                                background="transparent",
                                color=COLORS["text_muted"],
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="600",
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="8px",
                                padding="8px 16px",
                                cursor="pointer",
                                _hover={"background": "rgba(255, 255, 255, 0.05)"},
                            ),
                            game_button(
                                "🚀 Post Quest Now",
                                on_click=FeedState.create_quest,
                                variant="primary",
                                style={"padding": "8px 20px"},
                            ),
                            spacing="3",
                            width="100%",
                            align="center",
                            margin_top="10px",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                width=["90vw", "540px"],
                background_color="rgba(15, 23, 42, 0.96)",
                backdrop_filter="blur(24px)",
                border="1px solid rgba(255, 255, 255, 0.12)",
                box_shadow=f"0 25px 60px rgba(0, 0, 0, 0.7), 0 0 35px rgba(0, 245, 155, 0.15)",
                padding="24px",
                border_radius="16px",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            background_color="rgba(0, 0, 0, 0.75)",
            backdrop_filter="blur(8px)",
            z_index="9998",
        ),
    )
