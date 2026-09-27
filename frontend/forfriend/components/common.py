"""Reusable modern game-style components for ForFriend with Glassmorphism & Cyber Aesthetics."""
from typing import Optional
import reflex as rx
from ..styles.theme import (
    COLORS,
    FONTS,
    btn_primary_style,
    btn_secondary_style,
    btn_pink_style,
    game_card_style,
    game_input_style,
)
from ..state.base_state import BaseState


def game_button(
    text: str,
    on_click=None,
    variant: str = "primary",  # primary, secondary, pink, ghost
    icon: Optional[str] = None,
    **props,
) -> rx.Component:
    """Nút bấm phong cách Cyberpunk Modern Gaming với neon gradient và hover glow."""
    if variant == "secondary":
        base_style = btn_secondary_style
    elif variant == "pink":
        base_style = btn_pink_style
    elif variant == "ghost":
        base_style = {
            "font_family": FONTS["ui"],
            "font_size": "13px",
            "font_weight": "600",
            "padding": "10px 16px",
            "background": "rgba(255, 255, 255, 0.04)",
            "color": COLORS["text_main"],
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "border_radius": "8px",
            "cursor": "pointer",
            "transition": "all 200ms ease",
            "_hover": {
                "background": "rgba(255, 255, 255, 0.08)",
                "border_color": "rgba(255, 255, 255, 0.25)",
            },
        }
    else:
        base_style = btn_primary_style

    combined_style = {**base_style, **props.pop("style", {})}
    content = []
    if icon:
        content.append(rx.text(icon, margin_right="6px", font_size="14px"))
    content.append(rx.text(text))

    return rx.button(
        *content,
        on_click=on_click,
        style=combined_style,
        **props,
    )


def game_card(*children, **props) -> rx.Component:
    """Card container chuẩn Glassmorphism với viền phát sáng đa chiều."""
    combined_style = {**game_card_style, **props.pop("style", {})}
    return rx.box(
        *children,
        style=combined_style,
        **props,
    )


def game_input(
    placeholder: str,
    value,
    on_change,
    input_type: str = "text",
    **props,
) -> rx.Component:
    """Input hiện đại chuẩn Neo-Cyber, không bị ép chữ hay cắt viền."""
    combined_style = {**game_input_style, **props.pop("style", {})}
    return rx.input(
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        type=input_type,
        size="3",
        style=combined_style,
        **props,
    )


def lang_toggle_button() -> rx.Component:
    """Badge hiển thị ngôn ngữ hệ thống Tiếng Anh chuẩn Neo-Cyber."""
    return rx.box(
        rx.text("🇬🇧 ENG", font_family=FONTS["ui"], font_weight="700", font_size="11px", color=COLORS["neon_green"]),
        background="rgba(0, 245, 155, 0.08)",
        border=f"1px solid rgba(0, 245, 155, 0.3)",
        border_radius="9999px",
        padding="4px 10px",
    )


def pixel_title(
    text: str,
    size: str = "1.3rem",
    color: Optional[str] = None,
    use_pixel: bool = False,
    **props,
) -> rx.Component:
    """Heading hiện đại phong cách Gaming Display, hỗ trợ tiếng Việt trọn vẹn."""
    glow_color = color or COLORS["neon_green"]
    font_fam = FONTS["pixel"] if use_pixel else FONTS["heading"]
    return rx.heading(
        text,
        font_family=font_fam,
        font_size=size,
        font_weight="800",
        color=glow_color,
        text_shadow=f"0 0 16px {glow_color}66",
        letter_spacing="0.5px",
        **props,
    )


def star_rating(rating, max_stars: int = 5) -> rx.Component:
    """Hiển thị số sao uy tín ánh kim hiện đại."""
    return rx.hstack(
        rx.text(
            "★",
            color=COLORS["neon_gold"],
            font_size="14px",
            text_shadow="0 0 8px rgba(255, 230, 0, 0.6)",
        ),
        rx.text(
            rating,
            font_size="13px",
            font_family=FONTS["ui"],
            font_weight="700",
            color=COLORS["neon_gold"],
        ),
        spacing="1",
        align="center",
    )


def avatar_display(
    avatar_id,
    size: str = "48px",
    border_glow=True,
    **props,
) -> rx.Component:
    """Hiển thị avatar chibi retro sắc nét theo ID (1-15) kèm vòng sáng hiện đại."""
    border_style = rx.cond(border_glow, f"2px solid {COLORS['neon_green']}", "1px solid rgba(255, 255, 255, 0.12)")
    shadow = rx.cond(border_glow, f"0 0 12px {COLORS['neon_green']}66", "0 4px 10px rgba(0,0,0,0.3)")

    if isinstance(avatar_id, rx.Var):
        src_val = "/avatars/avatar_" + avatar_id.to(str) + ".png"
    elif isinstance(avatar_id, str) and (avatar_id.startswith("/") or avatar_id.startswith("http")):
        src_val = avatar_id
    else:
        raw = str(avatar_id or "1").replace("avatar_", "").replace("avatar-", "").replace(".png", "").lstrip("0")
        src_val = f"/avatars/avatar_{raw or '1'}.png"

    return rx.image(
        src=src_val,
        width=size,
        height=size,
        border_radius="50%",
        object_fit="cover",
        border=border_style,
        box_shadow=shadow,
        background="rgba(10, 10, 26, 0.6)",
        transition="all 200ms ease",
        _hover={"transform": "scale(1.05)"},
        **props,
    )


def status_badge(is_online, text: Optional[str] = None) -> rx.Component:
    """Badge trạng thái hiện đại dạng neon pill với chấm sáng pulse."""
    dot_color = rx.cond(is_online, COLORS["neon_green"], COLORS["text_muted"])
    default_label = rx.cond(is_online, "ONLINE", "OFFLINE")
    label = text if text is not None else default_label
    return rx.hstack(
        rx.box(
            width="8px",
            height="8px",
            border_radius="50%",
            background_color=dot_color,
            box_shadow=rx.cond(is_online, f"0 0 8px {COLORS['neon_green']}", "none"),
            class_name="pulse-dot",
        ),
        rx.text(
            label,
            font_family=FONTS["ui"],
            font_size="11px",
            font_weight="700",
            letter_spacing="0.5px",
            color=dot_color,
        ),
        spacing="2",
        align="center",
        padding="2px 8px",
        border_radius="9999px",
        background_color="rgba(255, 255, 255, 0.04)",
        border="1px solid rgba(255, 255, 255, 0.06)",
    )


def toast_banner() -> rx.Component:
    """Banner thông báo Toast kính mờ hiện đại."""
    return rx.cond(
        BaseState.show_toast,
        rx.box(
            rx.hstack(
                rx.text(
                    rx.cond(
                        BaseState.toast_type == "error",
                        "✕ ",
                        rx.cond(BaseState.toast_type == "warning", "⚠ ", "✓ "),
                    ),
                    font_weight="bold",
                    font_size="15px",
                ),
                rx.text(
                    BaseState.toast_message,
                    font_family=FONTS["ui"],
                    font_size="13px",
                    font_weight="600",
                ),
                rx.spacer(),
                rx.button(
                    "✕",
                    on_click=BaseState.dismiss_toast,
                    background="transparent",
                    color="inherit",
                    cursor="pointer",
                    padding="0 6px",
                    font_size="13px",
                    _hover={"opacity": "0.7"},
                ),
                align="center",
                width="100%",
                spacing="2",
            ),
            position="fixed",
            top="24px",
            right="24px",
            z_index="9999",
            background_color=rx.cond(
                BaseState.toast_type == "error",
                "rgba(255, 77, 109, 0.95)",
                rx.cond(BaseState.toast_type == "warning", "rgba(251, 191, 36, 0.95)", "rgba(0, 255, 136, 0.95)"),
            ),
            color="#04120a",
            padding="12px 20px",
            border_radius="10px",
            box_shadow="0 10px 30px rgba(0, 0, 0, 0.4), 0 0 15px rgba(0, 255, 136, 0.2)",
            max_width="440px",
            class_name="slide-in-up",
        ),
    )
