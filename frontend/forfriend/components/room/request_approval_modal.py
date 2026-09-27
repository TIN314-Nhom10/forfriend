"""Request Approval Modal: Host duyệt người gõ cửa xin vào phòng với Glassmorphism."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import avatar_display, game_button, pixel_title
from ...state.room_state import RoomState
from ...state.base_state import BaseState
from ...state.models import KnockRequestItem


def applicant_row(req: KnockRequestItem) -> rx.Component:
    """Từng hàng người xin vào phòng."""
    return rx.hstack(
        avatar_display(req.avatar_id, size="40px"),
        rx.vstack(
            rx.text(req.name, font_family=FONTS["ui"], font_weight="700", color=COLORS["text_main"], font_size="14px"),
            rx.text(req.school, font_family=FONTS["ui"], color=COLORS["text_muted"], font_size="12px"),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.button(
            "✓ Approve",
            on_click=RoomState.approve_user(req.id),
            font_family=FONTS["ui"],
            font_size="12px",
            font_weight="700",
            background=COLORS["neon_green"],
            color="#04120a",
            padding="6px 14px",
            border_radius="6px",
            cursor="pointer",
            _hover={"filter": "brightness(1.1)"},
        ),
        rx.button(
            "✕ Reject",
            on_click=RoomState.reject_user(req.id),
            font_family=FONTS["ui"],
            font_size="12px",
            font_weight="600",
            background="rgba(255, 77, 109, 0.1)",
            color=COLORS["danger"],
            border=f"1px solid rgba(255, 77, 109, 0.3)",
            padding="6px 14px",
            border_radius="6px",
            cursor="pointer",
            _hover={"background": "rgba(255, 77, 109, 0.2)"},
        ),
        spacing="3",
        align="center",
        width="100%",
        padding="12px 14px",
        background_color="rgba(255, 255, 255, 0.04)",
        border="1px solid rgba(255, 255, 255, 0.06)",
        border_radius="10px",
    )


def request_approval_modal() -> rx.Component:
    """Modal quản lý yêu cầu xin vào phòng của Host."""
    return rx.cond(
        RoomState.show_approval_modal,
        rx.center(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        pixel_title(
                            "🚪 KNOCK REQUESTS",
                            size="16px",
                            color=COLORS["neon_gold"],
                        ),
                        rx.spacer(),
                        rx.button("✕", on_click=RoomState.toggle_approval_modal, background="transparent", color="#fff", cursor="pointer"),
                        width="100%",
                        align="center",
                    ),
                    rx.cond(
                        RoomState.pending_requests.length() == 0,
                        rx.text(
                            "No pending knock requests.",
                            font_family=FONTS["ui"],
                            color=COLORS["text_muted"],
                            font_size="14px",
                        ),
                        rx.vstack(
                            rx.foreach(RoomState.pending_requests, applicant_row),
                            spacing="2",
                            width="100%",
                        ),
                    ),
                    spacing="4",
                    width="100%",
                ),
                width=["90vw", "480px"],
                background_color="rgba(18, 18, 38, 0.95)",
                backdrop_filter="blur(24px)",
                border="1px solid rgba(255, 255, 255, 0.12)",
                box_shadow="0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 230, 0, 0.15)",
                padding="24px",
                border_radius="14px",
            ),
            position="fixed",
            inset="0",
            background_color="rgba(0,0,0,0.75)",
            backdrop_filter="blur(8px)",
            z_index="1000",
        ),
    )
