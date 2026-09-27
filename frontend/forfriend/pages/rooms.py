"""Rooms Page: Sảnh phòng học ảo (Adventure Zones Lobby) phong cách Modern Cyber Gaming & Glassmorphism."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.common import pixel_title, game_button
from ..components.layout.game_layout import game_layout
from ..components.room.room_card import room_card
from ..components.room.create_room_modal import create_room_modal
from ..components.rating.rating_modal import rating_modal
from ..state.room_state import RoomState
from ..state.base_state import BaseState
from ..state.models import CategoryItem


def category_filter_pill(cat: CategoryItem) -> rx.Component:
    """Nút lọc theo danh mục phòng học dạng modern glass pill."""
    is_active = RoomState.selected_category_id == cat.id
    return rx.button(
        rx.hstack(
            rx.text(cat.icon, font_size="13px"),
            rx.text(cat.name),
            spacing="1",
            align="center",
        ),
        on_click=RoomState.set_category(cat.id),
        font_family=FONTS["ui"],
        font_size="12px",
        font_weight="600",
        background_color=rx.cond(is_active, COLORS["neon_cyan"], "rgba(255, 255, 255, 0.04)"),
        color=rx.cond(is_active, "#04120a", COLORS["text_main"]),
        border=rx.cond(is_active, f"1px solid {COLORS['neon_cyan']}", "1px solid rgba(255, 255, 255, 0.08)"),
        box_shadow=rx.cond(is_active, "0 0 12px rgba(0, 229, 255, 0.35)", "none"),
        padding="6px 14px",
        border_radius="9999px",
        cursor="pointer",
        transition="all 150ms ease",
        _hover={
            "border_color": COLORS["neon_cyan"],
            "background_color": rx.cond(is_active, COLORS["neon_cyan"], "rgba(0, 229, 255, 0.1)"),
            "transform": "translateY(-1px)",
        },
    )


def rooms_page() -> rx.Component:
    """Giao diện Sảnh phòng học ảo."""
    return game_layout(
        rx.box(
            create_room_modal(),
            rating_modal(),
            rx.vstack(
                # Top Header & Create Button
                rx.hstack(
                    rx.vstack(
                        pixel_title(
                            "🎮 STUDY ROOMS LOBBY",
                            size="22px",
                            color=COLORS["neon_cyan"],
                        ),
                        rx.text(
                            "Collaborative study rooms with WebRTC Video Call — Knock to join or create your own Zone",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    game_button(
                        "+ Open New Zone",
                        on_click=RoomState.toggle_create_modal,
                        variant="primary",
                        style={"padding": "10px 20px"},
                    ),
                    width="100%",
                    align="center",
                    wrap="wrap",
                ),
                # Categories Filter Bar
                rx.hstack(
                    rx.button(
                        "★ All",
                        on_click=RoomState.set_category(""),
                        font_family=FONTS["ui"],
                        font_size="12px",
                        font_weight="700",
                        background_color=rx.cond(RoomState.selected_category_id == "", COLORS["neon_cyan"], "rgba(255, 255, 255, 0.04)"),
                        color=rx.cond(RoomState.selected_category_id == "", "#04120a", COLORS["text_main"]),
                        border=rx.cond(RoomState.selected_category_id == "", f"1px solid {COLORS['neon_cyan']}", "1px solid rgba(255, 255, 255, 0.08)"),
                        box_shadow=rx.cond(RoomState.selected_category_id == "", "0 0 12px rgba(0, 229, 255, 0.35)", "none"),
                        padding="6px 14px",
                        border_radius="9999px",
                        cursor="pointer",
                        transition="all 150ms ease",
                        _hover={"transform": "translateY(-1px)"},
                    ),
                    rx.foreach(RoomState.categories, category_filter_pill),
                    spacing="2",
                    wrap="wrap",
                    padding_y="8px",
                    width="100%",
                ),
                # Rooms Grid List
                rx.cond(
                    RoomState.is_loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(color=COLORS["neon_cyan"], size="3"),
                            rx.text(
                                "Scanning open study rooms...",
                                font_family=FONTS["ui"],
                                font_size="14px",
                                font_weight="600",
                                color=COLORS["neon_cyan"],
                            ),
                            spacing="3",
                        ),
                        height="300px",
                        width="100%",
                    ),
                    rx.cond(
                        RoomState.rooms.length() == 0,
                        rx.center(
                            rx.vstack(
                                rx.box(
                                    rx.text("🏰", font_size="36px", color=COLORS["neon_cyan"]),
                                    padding="16px",
                                    border_radius="50%",
                                    background="rgba(0, 229, 255, 0.08)",
                                    border="1px solid rgba(0, 229, 255, 0.2)",
                                ),
                                rx.text(
                                    "No active study rooms in this category.",
                                    font_family=FONTS["ui"],
                                    font_size="15px",
                                    font_weight="600",
                                    color=COLORS["text_muted"],
                                ),
                                game_button(
                                    "Create First Zone",
                                    on_click=RoomState.toggle_create_modal,
                                    variant="primary",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            height="280px",
                            width="100%",
                        ),
                        rx.grid(
                            rx.foreach(RoomState.rooms, room_card),
                            columns=rx.breakpoints(initial="1", md="2"),
                            spacing="4",
                            width="100%",
                        ),
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
        ),
        on_mount=RoomState.load_lobby,
    )
