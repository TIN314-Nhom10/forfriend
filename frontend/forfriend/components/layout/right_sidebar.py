"""Right Sidebar Component: Hồ sơ người dùng, Active Quests và Recent Contacts theo chuẩn mockup."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import avatar_display
from ...state.base_state import BaseState


def right_sidebar() -> rx.Component:
    """Sidebar bên phải hiển thị thông tin Liam M., Level 14 Study Hero, Active Quests & Recent Contacts."""
    return rx.box(
        rx.vstack(
            # 1. Welcome User Card
            rx.box(
                rx.vstack(
                    # Circular Avatar with glowing aura
                    rx.center(
                        rx.box(
                            avatar_display(
                                rx.cond(BaseState.avatar_id != "", BaseState.avatar_id, "1"),
                                size="86px",
                                border_glow=True,
                            ),
                            padding="4px",
                            border_radius="50%",
                            background="radial-gradient(circle, rgba(44, 234, 163, 0.25) 0%, rgba(0, 210, 255, 0.15) 60%, transparent 100%)",
                        ),
                        width="100%",
                        padding_y="10px",
                    ),
                    rx.text(
                        rx.cond(
                            BaseState.is_authenticated,
                            "Welcome, " + BaseState.user_name,
                            "Welcome, Liam M.",
                        ),
                        font_family=FONTS["heading"],
                        font_size="18px",
                        font_weight="700",
                        color=COLORS["text_main"],
                        text_align="center",
                        width="100%",
                    ),
                    rx.text(
                        "Level 14 Study Hero",
                        font_family=FONTS["ui"],
                        font_size="13px",
                        color=COLORS["text_muted"],
                        text_align="center",
                        width="100%",
                    ),
                    # EXP Progress bar
                    rx.box(
                        rx.box(
                            width="68%",
                            height="5px",
                            border_radius="3px",
                            background="linear-gradient(90deg, #2ceaa3 0%, #00d2ff 100%)",
                            box_shadow="0 0 10px rgba(44, 234, 163, 0.5)",
                        ),
                        width="100%",
                        height="5px",
                        background="rgba(255, 255, 255, 0.08)",
                        border_radius="3px",
                        margin_y="8px",
                    ),
                    rx.text(
                        "Bio, cute chibi cat, gaming headset, and master unique study partners.",
                        font_family=FONTS["ui"],
                        font_size="12px",
                        color=COLORS["text_muted"],
                        line_height="1.5",
                        text_align="center",
                        padding_x="4px",
                    ),
                    spacing="1",
                    align="center",
                    width="100%",
                ),
                padding="18px",
                border_radius="16px",
                background_color="rgba(19, 34, 42, 0.8)",
                border="1px solid rgba(44, 234, 163, 0.2)",
                box_shadow="0 8px 24px rgba(0, 0, 0, 0.35)",
                width="100%",
            ),

            # 2. Active Quests Section
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Active Quests",
                        font_family=FONTS["ui"],
                        font_size="14px",
                        font_weight="700",
                        color=COLORS["text_main"],
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.text("View all", font_size="11px", color=COLORS["neon_green"], font_weight="700"),
                        href="/rooms",
                        text_decoration="none",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.link(
                    rx.box(
                        rx.hstack(
                            avatar_display("1", size="36px", border_glow=False),
                            rx.vstack(
                                rx.text(
                                    "Liam M.",
                                    font_family=FONTS["ui"],
                                    font_size="13px",
                                    font_weight="700",
                                    color=COLORS["text_main"],
                                ),
                                rx.text(
                                    "Uni: Study Hero",
                                    font_family=FONTS["ui"],
                                    font_size="11px",
                                    color=COLORS["text_muted"],
                                ),
                                rx.text(
                                    "Math Prep: Calculus II",
                                    font_family=FONTS["ui"],
                                    font_size="12px",
                                    font_weight="600",
                                    color=COLORS["neon_cyan"],
                                ),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.text("›", font_size="20px", color=COLORS["text_muted"]),
                            spacing="3",
                            align="center",
                            width="100%",
                            padding="10px",
                        ),
                        border_radius="12px",
                        background="rgba(255, 255, 255, 0.03)",
                        border="1px solid rgba(255, 255, 255, 0.06)",
                        width="100%",
                        cursor="pointer",
                        _hover={"background": "rgba(44, 234, 163, 0.08)", "border_color": COLORS["neon_green"]},
                    ),
                    href="/rooms",
                    width="100%",
                    text_decoration="none",
                ),
                spacing="2",
                width="100%",
                margin_top="6px",
            ),

            # 3. Recent Contacts Section
            rx.vstack(
                rx.text(
                    "Recent Contacts",
                    font_family=FONTS["ui"],
                    font_size="14px",
                    font_weight="700",
                    color=COLORS["text_main"],
                    width="100%",
                ),
                # Contact 1: Liam M.
                rx.link(
                    rx.hstack(
                        avatar_display("1", size="36px", border_glow=False),
                        rx.vstack(
                            rx.text("Liam M.", font_size="13px", font_weight="700", color=COLORS["text_main"]),
                            rx.text("Gaming Hub", font_size="11px", color=COLORS["text_muted"]),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.badge("Online", bg="rgba(44, 234, 163, 0.12)", color=COLORS["neon_green"], border_radius="9999px", font_size="10px", padding="2px 8px"),
                        spacing="2",
                        align="center",
                        width="100%",
                        padding="6px 8px",
                        border_radius="10px",
                        cursor="pointer",
                        _hover={"background": "rgba(44, 234, 163, 0.08)"},
                    ),
                    href="/chat",
                    width="100%",
                    text_decoration="none",
                ),
                # Contact 2: Chloe T.
                rx.link(
                    rx.hstack(
                        avatar_display("2", size="36px", border_glow=False),
                        rx.vstack(
                            rx.text("Chloe T.", font_size="13px", font_weight="700", color=COLORS["text_main"]),
                            rx.text("Reading", font_size="11px", color=COLORS["text_muted"]),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.badge("Active", bg="rgba(0, 210, 255, 0.12)", color=COLORS["neon_cyan"], border_radius="9999px", font_size="10px", padding="2px 8px"),
                        spacing="2",
                        align="center",
                        width="100%",
                        padding="6px 8px",
                        border_radius="10px",
                        cursor="pointer",
                        _hover={"background": "rgba(0, 210, 255, 0.08)"},
                    ),
                    href="/chat",
                    width="100%",
                    text_decoration="none",
                ),
                # Contact 3: Katlantlan
                rx.link(
                    rx.hstack(
                        avatar_display("5", size="36px", border_glow=False),
                        rx.vstack(
                            rx.text("Katlantlan", font_size="13px", font_weight="700", color=COLORS["text_main"]),
                            rx.text("Study Library", font_size="11px", color=COLORS["text_muted"]),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.badge("Reading", bg="rgba(251, 191, 36, 0.12)", color=COLORS["neon_gold"], border_radius="9999px", font_size="10px", padding="2px 8px"),
                        spacing="2",
                        align="center",
                        width="100%",
                        padding="6px 8px",
                        border_radius="10px",
                        cursor="pointer",
                        _hover={"background": "rgba(251, 191, 36, 0.08)"},
                    ),
                    href="/chat",
                    width="100%",
                    text_decoration="none",
                ),
                spacing="2",
                width="100%",
                margin_top="6px",
            ),
            spacing="4",
            width="100%",
        ),
        width=["100%", "100%", "280px", "300px"],
        padding_left=["0", "0", "16px"],
        display=["none", "none", "block", "block"],
    )
