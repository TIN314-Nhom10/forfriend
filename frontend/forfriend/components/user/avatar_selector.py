"""Avatar Selector Component: Lưới chọn 15 Student Avatars với Glassmorphism."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ...state.register_state import RegisterState
from ...state.base_state import BaseState

STUDENT_AVATARS = [
    (1, "Liam"),
    (2, "Chloe"),
    (3, "Ben"),
    (4, "Anya"),
    (5, "Katlantlan"),
    (6, "Alex"),
    (7, "Maya"),
    (8, "Leo"),
    (9, "Luna"),
    (10, "Noah"),
    (11, "Stella"),
    (12, "Kai"),
    (13, "Momo"),
    (14, "Ren"),
    (15, "Mia"),
]


def avatar_option(char_info: tuple[int, str]) -> rx.Component:
    """Từng ô avatar trong lưới với viền phát sáng khi chọn."""
    char_id, avatar_name = char_info
    is_selected = RegisterState.selected_avatar_id == char_id

    return rx.box(
        rx.vstack(
            rx.image(
                src=f"/avatars/avatar_{char_id}.png",
                width="52px",
                height="52px",
                border_radius="50%",
                object_fit="cover",
            ),
            rx.text(
                avatar_name,
                font_family=FONTS["ui"],
                font_size="11px",
                font_weight="700",
                color=rx.cond(is_selected, COLORS["neon_green"], COLORS["text_secondary"]),
                text_align="center",
            ),
            spacing="1",
            align="center",
        ),
        on_click=RegisterState.set_avatar(char_id),
        padding="8px 6px",
        border_radius="10px",
        cursor="pointer",
        background_color=rx.cond(is_selected, "rgba(0, 255, 136, 0.12)", "rgba(255, 255, 255, 0.03)"),
        border=rx.cond(is_selected, f"2px solid {COLORS['neon_green']}", "1px solid rgba(255, 255, 255, 0.08)"),
        box_shadow=rx.cond(is_selected, f"0 0 16px rgba(0, 255, 136, 0.4)", "none"),
        transition="all 200ms ease",
        _hover={
            "border_color": COLORS["neon_green"],
            "transform": "scale(1.06)",
        },
    )


def avatar_selector() -> rx.Component:
    """Lưới 15 Student Avatars cho bước tạo tài khoản."""
    return rx.vstack(
        rx.text(
            ">> SELECT YOUR AVATAR <<",
            font_family=FONTS["ui"],
            font_size="13px",
            font_weight="700",
            color=COLORS["neon_pink"],
            letter_spacing="0.5px",
        ),
        rx.grid(
            *[avatar_option(c) for c in STUDENT_AVATARS],
            columns="5",
            spacing="2",
            width="100%",
        ),
        spacing="3",
        width="100%",
    )
