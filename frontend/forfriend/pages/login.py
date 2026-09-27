"""Login Page: Màn hình Đăng nhập phong cách Neo-Cyber Student với Glassmorphism."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.common import game_button, game_input, pixel_title, toast_banner, lang_toggle_button
from ..state.auth_state import AuthState
from ..state.base_state import BaseState


def login_page() -> rx.Component:
    """Giao diện đăng nhập hiện đại phong cách Neo-Cyber Glass."""
    return rx.box(
        toast_banner(),
        rx.center(
            rx.vstack(
                # Neo-Cyber Box
                rx.box(
                    rx.vstack(
                        # Header
                        rx.vstack(
                            rx.box(
                                rx.text(
                                    "★ STUDY PARTNER PLATFORM ★",
                                    font_family=FONTS["ui"],
                                    font_weight="700",
                                    font_size="10px",
                                    color=COLORS["neon_green"],
                                    letter_spacing="1px",
                                ),
                                padding="4px 12px",
                                border_radius="9999px",
                                background="rgba(0, 245, 155, 0.1)",
                                border=f"1px solid rgba(0, 245, 155, 0.3)",
                            ),
                            pixel_title("FORFRIEND", size="34px", color=COLORS["neon_green"]),
                            rx.text(
                                "Student Study Partner Platform",
                                font_family=FONTS["ui"],
                                font_size="14px",
                                font_weight="600",
                                color=COLORS["neon_cyan"],
                            ),
                            spacing="2",
                            align="center",
                            margin_bottom="18px",
                        ),
                        # Form Fields
                        rx.vstack(
                            rx.text(
                                "Student Email:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "nguyenvana@ftu.edu.vn",
                                AuthState.login_email,
                                AuthState.set_login_email,
                            ),
                            rx.text(
                                "Password:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "••••••••",
                                AuthState.login_password,
                                AuthState.set_login_password,
                                input_type="password",
                            ),
                            rx.cond(
                                AuthState.login_error != "",
                                rx.text(
                                    AuthState.login_error,
                                    color=COLORS["danger"],
                                    font_family=FONTS["ui"],
                                    font_size="13px",
                                    font_weight="bold",
                                ),
                            ),
                            # Login Button
                            game_button(
                                rx.cond(
                                    AuthState.is_loading,
                                    "...",
                                    "▶ START (LOG IN)",
                                ),
                                on_click=AuthState.handle_login,
                                variant="primary",
                                style={"width": "100%", "padding": "12px", "margin_top": "10px", "font_size": "14px"},
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # Demo Accounts Quick Fill & 1-Click
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("⚡ QUICK TEST ACCOUNTS:", font_family=FONTS["ui"], font_weight="700", font_size="11px", color=COLORS["neon_gold"]),
                                    rx.spacer(),
                                    rx.button(
                                        "⚡ 1-Click Login",
                                        on_click=BaseState.login_as_demo,
                                        size="1",
                                        background=COLORS["neon_green"],
                                        color="#04120a",
                                        font_weight="700",
                                        border_radius="6px",
                                        cursor="pointer",
                                    ),
                                    width="100%",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.button(
                                        "👤 Student 1 (FTU)",
                                        on_click=AuthState.fill_demo("nguyenvana@ftu.edu.vn", "Password123!"),
                                        font_family=FONTS["ui"],
                                        font_size="12px",
                                        font_weight="600",
                                        background="rgba(0, 245, 155, 0.08)",
                                        color=COLORS["neon_green"],
                                        border=f"1px solid rgba(0, 245, 155, 0.3)",
                                        border_radius="8px",
                                        padding="5px 10px",
                                        cursor="pointer",
                                        _hover={"background": "rgba(0, 245, 155, 0.18)"},
                                    ),
                                    rx.button(
                                        "👤 Student 2 (NEU)",
                                        on_click=AuthState.fill_demo("tranthib@neu.edu.vn", "Password123!"),
                                        font_family=FONTS["ui"],
                                        font_size="12px",
                                        font_weight="600",
                                        background="rgba(0, 210, 255, 0.08)",
                                        color=COLORS["neon_cyan"],
                                        border=f"1px solid rgba(0, 210, 255, 0.3)",
                                        border_radius="8px",
                                        padding="5px 10px",
                                        cursor="pointer",
                                        _hover={"background": "rgba(0, 210, 255, 0.18)"},
                                    ),
                                    spacing="2",
                                    wrap="wrap",
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            padding="14px",
                            background_color="rgba(11, 15, 25, 0.7)",
                            border="1px solid rgba(255, 255, 255, 0.08)",
                            border_radius="10px",
                            margin_top="16px",
                            width="100%",
                        ),
                        # Link to Register
                        rx.hstack(
                            rx.text(
                                "New Student?",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                color=COLORS["text_muted"],
                            ),
                            rx.link(
                                "Create Account Now →",
                                href="/register",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_pink"],
                                text_decoration="none",
                                _hover={"text_decoration": "underline"},
                            ),
                            spacing="2",
                            justify="center",
                            margin_top="16px",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    background_color="rgba(15, 23, 42, 0.95)",
                    backdrop_filter="blur(24px)",
                    border="1px solid rgba(255, 255, 255, 0.12)",
                    box_shadow=f"0 25px 60px rgba(0, 0, 0, 0.7), 0 0 35px rgba(0, 245, 155, 0.15)",
                    padding=["24px", "36px"],
                    border_radius="18px",
                    max_width="440px",
                    width="95%",
                ),
                # Footer note
                rx.text(
                    "© 2026 ForFriend Course Project • 100% Pure Python",
                    font_size="12px",
                    color=COLORS["text_muted"],
                    margin_top="24px",
                ),
                align="center",
                spacing="2",
            ),
            min_height="100vh",
            padding="20px",
        ),
        background_color="transparent",
        min_height="100vh",
        width="100%",
    )
