"""Room Card Component: Thẻ hiển thị phòng học ảo trong Sảnh với Glassmorphism & Cyber Aesthetics."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import game_card, avatar_display, game_button
from ...state.room_state import RoomState
from ...state.base_state import BaseState
from ...state.models import RoomItem


def room_card(room: RoomItem) -> rx.Component:
    """Card hiển thị 1 Adventure Zone phòng học phong cách Cyber Glass."""
    return game_card(
        rx.vstack(
            # Top Host Info & Category
            rx.hstack(
                avatar_display(room.host_avatar_id, size="44px"),
                rx.vstack(
                    rx.text(
                        room.title,
                        font_family=FONTS["heading"],
                        font_size="16px",
                        font_weight="700",
                        color=COLORS["text_main"],
                    ),
                    rx.text(
                        f"Host: {room.host_name}",
                        font_family=FONTS["ui"],
                        font_size="12px",
                        color=COLORS["text_muted"],
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.badge(
                    rx.hstack(
                        rx.text(room.category_icon, font_size="13px"),
                        rx.text(room.category_name, font_weight="600"),
                        spacing="1",
                    ),
                    bg="rgba(0, 229, 255, 0.08)",
                    color=COLORS["neon_cyan"],
                    border="1px solid rgba(0, 229, 255, 0.25)",
                    font_family=FONTS["ui"],
                    font_size="11px",
                    padding="3px 10px",
                    border_radius="9999px",
                ),
                width="100%",
                align="center",
            ),
            # Topic description
            rx.cond(
                room.topic != "",
                rx.text(
                    room.topic,
                    font_family=FONTS["body"],
                    font_size="13px",
                    color="#94a3b8",
                    margin_top="10px",
                    line_height="1.5",
                ),
            ),
            # Player Count & Action Bar
            rx.hstack(
                rx.hstack(
                    rx.text("👥", font_size="13px"),
                    rx.hstack(
                        rx.text(
                            room.current_participants,
                            font_family=FONTS["pixel"],
                            font_size="11px",
                            color=rx.cond(room.is_full, COLORS["danger"], COLORS["neon_green"]),
                        ),
                        rx.text("/", font_size="12px", color=COLORS["text_muted"]),
                        rx.text(
                            room.max_participants,
                            font_family=FONTS["pixel"],
                            font_size="11px",
                            color=COLORS["text_muted"],
                        ),
                        rx.text(
                            " STUDENTS",
                            font_family=FONTS["ui"],
                            font_size="11px",
                            font_weight="700",
                            color=COLORS["text_muted"],
                        ),
                        spacing="1",
                    ),
                    spacing="2",
                    align="center",
                    padding="4px 10px",
                    border_radius="6px",
                    background="rgba(255, 255, 255, 0.03)",
                    border="1px solid rgba(255, 255, 255, 0.06)",
                ),
                rx.spacer(),
                rx.cond(
                    room.is_my_room,
                    game_button(
                        "⚔ Enter Room (Host)",
                        on_click=RoomState.enter_room(room.id),
                        variant="primary",
                        style={"font_size": "12px", "padding": "6px 14px"},
                    ),
                    rx.cond(
                        room.is_full,
                        rx.button(
                            "Room Full",
                            disabled=True,
                            font_family=FONTS["ui"],
                            font_size="12px",
                            font_weight="600",
                            background="rgba(255, 255, 255, 0.04)",
                            color=COLORS["text_muted"],
                            border="1px solid rgba(255, 255, 255, 0.08)",
                            border_radius="8px",
                            padding="6px 14px",
                        ),
                        game_button(
                            "🚪 Knock to Join",
                            on_click=RoomState.request_join(room.id),
                            variant="secondary",
                            style={"font_size": "12px", "padding": "6px 14px"},
                        ),
                    ),
                ),
                width="100%",
                align="center",
                margin_top="14px",
            ),
            spacing="1",
            width="100%",
        ),
        width="100%",
    )
