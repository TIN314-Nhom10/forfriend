"""Register Page: Màn hình Tạo Hero & Chọn 15 Avatar Chibi phong cách Modern Cyber Gaming."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.common import game_button, game_input, pixel_title, toast_banner, lang_toggle_button
from ..components.user.avatar_selector import avatar_selector
from ..state.register_state import RegisterState
from ..state.base_state import BaseState


def register_page() -> rx.Component:
    """Giao diện tạo nhân vật Hero phong cách Cyber Glass."""
    return rx.box(
        toast_banner(),
        rx.center(
            rx.box(
                rx.vstack(
                    # Header
                    rx.vstack(
                        rx.box(
                            rx.text(
                                "★ STUDENT REGISTRATION ★",
                                font_family=FONTS["pixel"],
                                font_size="9px",
                                color=COLORS["neon_green"],
                                class_name="pixel-blink",
                            ),
                            padding="4px 10px",
                            border_radius="9999px",
                            background="rgba(0, 255, 136, 0.08)",
                            border=f"1px solid rgba(0, 255, 136, 0.25)",
                        ),
                        pixel_title(
                            "CREATE ACCOUNT",
                            size="28px",
                            color=COLORS["neon_pink"],
                        ),
                        rx.text(
                            "Enter your student details and select your profile avatar",
                            font_family=FONTS["ui"],
                            font_size="14px",
                            color=COLORS["text_muted"],
                        ),
                        spacing="2",
                        align="center",
                        margin_bottom="18px",
                    ),
                    # Form Grid: Inputs on Left, 15-Avatar Grid on Right (Desktop)
                    rx.hstack(
                        # Left: Form inputs
                        rx.vstack(
                            rx.text(
                                "Full Name:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "Nguyen Van A",
                                RegisterState.name,
                                RegisterState.set_name,
                            ),
                            rx.text(
                                "Student Email (.edu.vn):",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "nguyenvana@ftu.edu.vn",
                                RegisterState.email,
                                RegisterState.set_email,
                            ),
                            rx.text(
                                "Password (At least 8 chars):",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "••••••••",
                                RegisterState.password,
                                RegisterState.set_password,
                                input_type="password",
                            ),
                            rx.text(
                                "University:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "Foreign Trade University (FTU)",
                                RegisterState.school,
                                RegisterState.set_school,
                            ),
                            rx.text(
                                "City:",
                                font_family=FONTS["ui"],
                                font_size="13px",
                                font_weight="700",
                                color=COLORS["neon_cyan"],
                            ),
                            game_input(
                                "Ha Noi",
                                RegisterState.city,
                                RegisterState.set_city,
                            ),
                            spacing="2",
                            width=["100%", "300px"],
                        ),
                        # Right: 15-Avatar Grid
                        rx.box(
                            avatar_selector(),
                            flex="1",
                            padding_left=["0", "16px"],
                        ),
                        spacing="5",
                        wrap="wrap",
                        align="start",
                        width="100%",
                    ),
                    # Error Message
                    rx.cond(
                        RegisterState.error_message != "",
                        rx.text(
                            RegisterState.error_message,
                            color=COLORS["danger"],
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="bold",
                            margin_top="12px",
                        ),
                    ),
                    # Register Button
                    game_button(
                        rx.cond(
                            RegisterState.is_loading,
                            "CREATING ACCOUNT...",
                            "CREATE ACCOUNT & ENTER",
                        ),
                        on_click=RegisterState.handle_register,
                        variant="primary",
                        style={"width": "100%", "padding": "13px", "margin_top": "16px", "font_size": "14px"},
                    ),
                    # Back to Login
                    rx.hstack(
                        rx.text(
                            "Already have an account?",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            color=COLORS["text_muted"],
                        ),
                        rx.link(
                            "Login here →",
                            href="/login",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_green"],
                            text_decoration="none",
                            _hover={"text_decoration": "underline"},
                        ),
                        spacing="2",
                        justify="center",
                        margin_top="12px",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                background_color="rgba(18, 18, 38, 0.8)",
                backdrop_filter="blur(24px)",
                border="1px solid rgba(255, 255, 255, 0.1)",
                box_shadow="0 20px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(255, 0, 127, 0.15)",
                padding=["24px", "36px"],
                border_radius="16px",
                max_width="780px",
                width="95%",
            ),
            min_height="100vh",
            padding="24px",
        ),
        background_color="transparent",
        min_height="100vh",
        width="100%",
    )
