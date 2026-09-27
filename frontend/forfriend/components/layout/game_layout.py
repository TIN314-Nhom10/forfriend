"""Game Layout với Sidebar điều hướng phong cách Neo-Cyber Student (Discord Nitro + Raycast Gaming Hub)."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ..common import avatar_display, status_badge, toast_banner, lang_toggle_button
from ...state.base_state import BaseState


def nav_item(icon: str, label: str, href: str) -> rx.Component:
    """Mục menu hiện đại chuẩn Neo-Cyber với hover glow và viền accent mượt mà."""
    return rx.link(
        rx.hstack(
            rx.text(icon, font_size="17px"),
            rx.text(
                label,
                font_family=FONTS["ui"],
                font_size="13px",
                font_weight="600",
                letter_spacing="0.3px",
            ),
            spacing="3",
            align="center",
            padding="10px 16px",
            border_radius="10px",
            width="100%",
            transition="all 200ms ease",
            _hover={
                "background_color": "rgba(0, 245, 155, 0.08)",
                "color": COLORS["neon_green"],
                "transform": "translateX(4px)",
                "border_left": f"3px solid {COLORS['neon_green']}",
            },
        ),
        href=href,
        color=COLORS["text_muted"],
        text_decoration="none",
        width="100%",
    )


def game_sidebar() -> rx.Component:
    """Thanh điều hướng Sidebar chuẩn Neo-Cyber."""
    return rx.box(
        rx.vstack(
            # Brand Header with Green Owl Logo
            rx.vstack(
                rx.hstack(
                    rx.html("""
                    <svg width="34" height="34" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 6C13.3726 6 8 11.3726 8 18C8 26 13 32 20 34C27 32 32 26 32 18C32 11.3726 26.6274 6 20 6Z" fill="#13222a" stroke="#2ceaa3" stroke-width="2.5"/>
                        <path d="M10 11C11.5 8 14.5 6.5 17 6.5" stroke="#2ceaa3" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M30 11C28.5 8 25.5 6.5 23 6.5" stroke="#2ceaa3" stroke-width="2.5" stroke-linecap="round"/>
                        <circle cx="15.5" cy="18" r="4.5" stroke="#2ceaa3" stroke-width="2" fill="#0b1319"/>
                        <circle cx="15.5" cy="18" r="2" fill="#2ceaa3"/>
                        <circle cx="24.5" cy="18" r="4.5" stroke="#2ceaa3" stroke-width="2" fill="#0b1319"/>
                        <circle cx="24.5" cy="18" r="2" fill="#2ceaa3"/>
                        <path d="M18.5 21L20 24L21.5 21" stroke="#2ceaa3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M16 28C18 29.5 22 29.5 24 28" stroke="#2ceaa3" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                    """),
                    rx.heading(
                        "ForFriend",
                        font_family=FONTS["heading"],
                        font_size="21px",
                        font_weight="800",
                        color=COLORS["text_main"],
                        letter_spacing="0.5px",
                    ),
                    spacing="3",
                    align="center",
                ),
                padding="20px 18px 18px 18px",
                width="100%",
                border_bottom="1px solid rgba(255, 255, 255, 0.08)",
            ),
            # Navigation Links (Matching reference design)
            rx.vstack(
                nav_item("🏠", "Dashboard", "/"),
                nav_item("🔍", "Discover Partners", "/feed"),
                nav_item("👥", "Study Groups", "/rooms"),
                nav_item("💬", "Messages", "/friends"),
                nav_item("👤", "Profile", "/profile"),
                nav_item("⚙️", "Settings", "/profile"),
                spacing="2",
                padding="18px 12px",
                width="100%",
            ),
            rx.spacer(),
            # User Bottom Profile Card
            rx.box(
                rx.cond(
                    BaseState.is_authenticated,
                    # Authenticated User
                    rx.vstack(
                        rx.hstack(
                            avatar_display(BaseState.avatar_id, size="42px"),
                            rx.vstack(
                                rx.text(
                                    BaseState.user_name,
                                    font_family=FONTS["ui"],
                                    font_size="13px",
                                    font_weight="700",
                                    color=COLORS["text_main"],
                                    max_width="120px",
                                    overflow="hidden",
                                    text_overflow="ellipsis",
                                    white_space="nowrap",
                                ),
                                status_badge(True, "ONLINE"),
                                spacing="1",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                            width="100%",
                        ),
                        rx.button(
                            "🚪 Logout",
                            on_click=BaseState.logout_user,
                            font_family=FONTS["ui"],
                            font_size="11px",
                            font_weight="600",
                            background="rgba(244, 63, 94, 0.08)",
                            color=COLORS["danger"],
                            border=f"1px solid rgba(244, 63, 94, 0.25)",
                            border_radius="8px",
                            padding="6px 12px",
                            width="100%",
                            cursor="pointer",
                            transition="all 150ms ease",
                            _hover={
                                "background": "rgba(244, 63, 94, 0.2)",
                                "border_color": COLORS["danger"],
                            },
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    # Guest User (Chưa đăng nhập)
                    rx.vstack(
                        rx.hstack(
                            avatar_display("1", size="38px", border_glow=False),
                            rx.vstack(
                                rx.text(
                                    "Guest",
                                    font_family=FONTS["ui"],
                                    font_size="13px",
                                    font_weight="700",
                                    color=COLORS["text_muted"],
                                ),
                                status_badge(False, "GUEST"),
                                spacing="1",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                            width="100%",
                        ),
                        rx.button(
                            "⚡ 1-Click Demo Login",
                            on_click=BaseState.login_as_demo,
                            font_family=FONTS["ui"],
                            font_size="11px",
                            font_weight="700",
                            background=COLORS["neon_green"],
                            color="#04120a",
                            border="none",
                            border_radius="8px",
                            padding="6px 12px",
                            width="100%",
                            cursor="pointer",
                            box_shadow=f"0 0 10px {COLORS['neon_green']}44",
                            _hover={"filter": "brightness(1.1)"},
                        ),
                        rx.link(
                            rx.button(
                                "🔑 Login / Register",
                                font_family=FONTS["ui"],
                                font_size="11px",
                                font_weight="600",
                                background="rgba(255, 255, 255, 0.05)",
                                color=COLORS["text_main"],
                                border="1px solid rgba(255, 255, 255, 0.1)",
                                border_radius="8px",
                                padding="6px 12px",
                                width="100%",
                                cursor="pointer",
                            ),
                            href="/login",
                            width="100%",
                            text_decoration="none",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                padding="14px",
                margin="12px",
                border_radius="12px",
                border="1px solid rgba(255, 255, 255, 0.08)",
                background_color="rgba(15, 23, 42, 0.8)",
                box_shadow="0 4px 20px rgba(0, 0, 0, 0.3)",
            ),
            height="100vh",
            spacing="0",
            width="100%",
        ),
        width=["100%", "260px"],
        background_color="rgba(11, 15, 25, 0.88)",
        backdrop_filter="blur(24px)",
        border_right="1px solid rgba(255, 255, 255, 0.08)",
        position="sticky",
        top="0",
        z_index="100",
    )


def game_layout(*children, **props) -> rx.Component:
    """Wrapper layout chính chứa Sidebar và khu vực nội dung glassmorphism Neo-Cyber."""
    return rx.box(
        toast_banner(),
        rx.hstack(
            game_sidebar(),
            rx.box(
                *children,
                flex="1",
                min_height="100vh",
                background_color="transparent",
                padding=["16px", "24px", "32px"],
                overflow_y="auto",
                max_height="100vh",
            ),
            spacing="0",
            align="start",
            width="100%",
        ),
        background_color="transparent",
        min_height="100vh",
        width="100%",
        **props,
    )
