"""Rating Modal Component: Popup đánh giá sao cho đồng đội sau buổi học với Glassmorphism."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import avatar_display, game_button, pixel_title
from ...state.rating_state import RatingState
from ...state.base_state import BaseState
from ...state.models import TeammateItem


def star_button(idx: int) -> rx.Component:
    """Nút bấm chọn số sao."""
    is_active = RatingState.stars >= idx
    return rx.button(
        "★",
        on_click=RatingState.set_stars(idx),
        background="transparent",
        color=rx.cond(is_active, COLORS["neon_gold"], "#3a3a5c"),
        font_size="24px",
        cursor="pointer",
        padding="0 2px",
        text_shadow=rx.cond(is_active, "0 0 10px rgba(255, 230, 0, 0.7)", "none"),
        transition="all 150ms ease",
        _hover={"transform": "scale(1.2)"},
    )


def teammate_chip(user: TeammateItem) -> rx.Component:
    """Chip chọn bạn học để đánh giá dạng modern glass pill."""
    is_sel = RatingState.selected_user_id == user.id
    return rx.box(
        rx.hstack(
            avatar_display(user.avatar_id, size="30px"),
            rx.text(user.name, font_family=FONTS["ui"], font_size="13px", font_weight="600", color=COLORS["text_main"]),
            spacing="2",
            align="center",
        ),
        on_click=RatingState.select_user(user.id, user.name, user.avatar_id),
        padding="6px 14px",
        border_radius="9999px",
        cursor="pointer",
        background_color=rx.cond(is_sel, "rgba(255, 230, 0, 0.15)", "rgba(255, 255, 255, 0.04)"),
        border=rx.cond(is_sel, f"1px solid {COLORS['neon_gold']}", "1px solid rgba(255, 255, 255, 0.08)"),
        box_shadow=rx.cond(is_sel, "0 0 12px rgba(255, 230, 0, 0.3)", "none"),
        transition="all 150ms ease",
    )


def rating_modal() -> rx.Component:
    """Modal popup đánh giá bạn học sau khi rời phòng."""
    return rx.cond(
        RatingState.show_modal,
        rx.center(
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        pixel_title(
                            "★ RATE YOUR ALLY ★",
                            size="16px",
                            color=COLORS["neon_gold"],
                        ),
                        rx.spacer(),
                        rx.button("✕", on_click=RatingState.close_modal, background="transparent", color="#fff", cursor="pointer"),
                        width="100%",
                        align="center",
                    ),
                    rx.text(
                        "Leave reputation rating for your study partner!",
                        font_family=FONTS["ui"],
                        font_size="13px",
                        color=COLORS["text_muted"],
                    ),
                    # Teammates selector
                    rx.text(
                        "Select Study Partner:",
                        font_family=FONTS["ui"],
                        font_size="13px",
                        font_weight="700",
                        color=COLORS["neon_cyan"],
                    ),
                    rx.hstack(
                        rx.foreach(RatingState.pending_users, teammate_chip),
                        spacing="2",
                        wrap="wrap",
                        width="100%",
                    ),
                    # Target info & Star picker
                    rx.vstack(
                        rx.hstack(
                            avatar_display(RatingState.selected_user_avatar, size="48px"),
                            rx.vstack(
                                rx.text(RatingState.selected_user_name, font_family=FONTS["ui"], font_weight="700", color=COLORS["text_main"], font_size="15px"),
                                rx.hstack(
                                    *[star_button(i) for i in range(1, 6)],
                                    spacing="1",
                                ),
                                spacing="1",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                            padding="14px",
                            background_color="rgba(255, 255, 255, 0.04)",
                            border="1px solid rgba(255, 255, 255, 0.08)",
                            border_radius="10px",
                        ),
                        # Comment input
                        rx.text_area(
                            placeholder="Enter comments on study attitude, teamwork...",
                            value=RatingState.comment,
                            on_change=RatingState.set_comment,
                            background_color="rgba(10, 10, 24, 0.8)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            color=COLORS["text_main"],
                            font_family=FONTS["body"],
                            font_size="14px",
                            padding="12px",
                            border_radius="8px",
                            min_height="80px",
                            width="100%",
                            outline="none",
                            _focus={"border_color": COLORS["neon_gold"], "box_shadow": "0 0 0 3px rgba(255, 230, 0, 0.2)"},
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    # Submit button
                    rx.hstack(
                        rx.spacer(),
                        rx.button(
                            "Close",
                            on_click=RatingState.close_modal,
                            background="transparent",
                            color=COLORS["text_muted"],
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="600",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="8px",
                            padding="8px 16px",
                            cursor="pointer",
                        ),
                        game_button(
                            "★ Submit Rating",
                            on_click=RatingState.submit_rating,
                            variant="primary",
                        ),
                        spacing="3",
                        width="100%",
                        align="center",
                    ),
                    spacing="4",
                    width="100%",
                ),
                width=["90vw", "480px"],
                background_color="rgba(18, 18, 38, 0.95)",
                backdrop_filter="blur(24px)",
                border="1px solid rgba(255, 230, 0, 0.3)",
                box_shadow="0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 230, 0, 0.15)",
                padding="24px",
                border_radius="14px",
            ),
            position="fixed",
            inset="0",
            background_color="rgba(0, 0, 0, 0.75)",
            backdrop_filter="blur(8px)",
            z_index="1000",
        ),
    )
