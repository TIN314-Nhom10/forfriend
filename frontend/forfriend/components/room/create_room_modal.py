"""Create Room Modal: Popup tạo Adventure Zone phòng học mới với Glassmorphism."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import game_input, game_button, pixel_title
from ...state.room_state import RoomState
from ...state.base_state import BaseState
from ...state.models import CategoryItem


def category_option(cat: CategoryItem) -> rx.Component:
    """Từng option môn học trong danh sách dạng modern chip."""
    is_sel = RoomState.new_room_category_id == cat.id
    return rx.box(
        rx.hstack(
            rx.text(cat.icon, font_size="13px"),
            rx.text(cat.name, font_family=FONTS["ui"], font_size="12px", font_weight="600"),
            spacing="1",
            align="center",
            color=rx.cond(is_sel, "#04120a", COLORS["text_main"]),
        ),
        on_click=RoomState.set_new_room_category_id(cat.id),
        padding="6px 12px",
        border_radius="9999px",
        cursor="pointer",
        background_color=rx.cond(is_sel, COLORS["neon_green"], "rgba(255, 255, 255, 0.04)"),
        border=rx.cond(is_sel, f"1px solid {COLORS['neon_green']}", "1px solid rgba(255, 255, 255, 0.08)"),
        box_shadow=rx.cond(is_sel, "0 0 10px rgba(0, 255, 136, 0.3)", "none"),
        transition="all 150ms ease",
    )


def create_room_modal() -> rx.Component:
    """Modal tạo phòng học mới phong cách Cyber Glass."""
    return rx.cond(
        RoomState.show_create_modal,
        rx.center(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        pixel_title(
                            "+ CREATE NEW STUDY ROOM",
                            size="16px",
                            color=COLORS["neon_green"],
                        ),
                        rx.spacer(),
                        rx.button(
                            "✕",
                            on_click=RoomState.toggle_create_modal,
                            background="transparent",
                            color=COLORS["text_muted"],
                            cursor="pointer",
                            font_size="16px",
                            _hover={"color": "#ffffff"},
                        ),
                        width="100%",
                        align="center",
                    ),
                    # Auth Banner if Guest
                    rx.cond(
                        ~BaseState.is_authenticated,
                        rx.box(
                            rx.hstack(
                                rx.text("⚡", font_size="18px"),
                                rx.vstack(
                                    rx.text(
                                        "You are in guest mode. Log in to open a room:",
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
                    # Form
                    rx.vstack(
                        rx.text(
                            "Room Title:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input(
                            "e.g., Calculus 1 Exam Prep Group",
                            RoomState.new_room_title,
                            RoomState.set_new_room_title,
                        ),
                        rx.text(
                            "Study Topic / Goals:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input(
                            "e.g., Practice Derivatives & Integrals problems",
                            RoomState.new_room_topic,
                            RoomState.set_new_room_topic,
                        ),
                        rx.text(
                            "Select Subject Category:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        rx.hstack(
                            rx.foreach(RoomState.categories, category_option),
                            spacing="2",
                            wrap="wrap",
                            max_height="130px",
                            overflow_y="auto",
                            width="100%",
                            padding_y="4px",
                        ),
                        # Max participants
                        rx.hstack(
                            rx.text(
                                "Max Participants:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_gold"],
                            ),
                            rx.select(
                                ["2", "4", "6", "8", "10"],
                                value=RoomState.new_room_max.to_string(),
                                on_change=RoomState.set_new_room_max,
                                background_color="rgba(10, 10, 24, 0.8)",
                                color=COLORS["neon_green"],
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="8px",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                padding="4px 10px",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        # Error Message
                        rx.cond(
                            RoomState.create_error != "",
                            rx.text(RoomState.create_error, color=COLORS["danger"], font_family=FONTS["ui"], font_size="13px", font_weight="bold"),
                        ),
                        # Action Row
                        rx.hstack(
                            rx.spacer(),
                            rx.button(
                                "Cancel",
                                on_click=RoomState.toggle_create_modal,
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
                                "🎮 Create Zone",
                                on_click=RoomState.create_room,
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
                width=["90vw", "520px"],
                background_color="rgba(18, 18, 38, 0.95)",
                backdrop_filter="blur(24px)",
                border="1px solid rgba(255, 255, 255, 0.12)",
                box_shadow="0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(0, 229, 255, 0.15)",
                padding="24px",
                border_radius="14px",
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
