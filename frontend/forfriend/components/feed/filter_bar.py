"""Filter Bar Component: Dropdown bộ lọc Subject, Level, Time Zone, Availability và Weekly pill."""
import reflex as rx
from ...styles.theme import COLORS, FONTS
from ...state.feed_state import FeedState


def filter_dropdown(label: str, options: list[str], current_val, on_change) -> rx.Component:
    """Từng dropdown trong thanh filter chuẩn giao diện mockup."""
    return rx.vstack(
        rx.text(
            label,
            font_family=FONTS["ui"],
            font_size="11px",
            font_weight="600",
            color=COLORS["text_muted"],
        ),
        rx.select(
            options,
            value=current_val,
            on_change=on_change,
            font_family=FONTS["ui"],
            font_size="13px",
            color=COLORS["text_main"],
            background_color="rgba(19, 34, 42, 0.9)",
            border="1px solid rgba(255, 255, 255, 0.1)",
            border_radius="10px",
            padding="6px 12px",
            height="38px",
            cursor="pointer",
            _hover={"border_color": COLORS["neon_green"]},
            _focus={"border_color": COLORS["neon_green"]},
        ),
        spacing="1",
        align="start",
    )


def filter_bar() -> rx.Component:
    """Thanh lọc 4 dropdowns + Weekly pill button theo mockup ForFriend."""
    return rx.box(
        rx.hstack(
            filter_dropdown(
                "Subject",
                ["All Subjects", "Python", "Mathematics", "AI & ML", "Web Dev", "Design"],
                rx.cond(FeedState.filter_tag != "", FeedState.filter_tag, "All Subjects"),
                FeedState.on_subject_change,
            ),
            filter_dropdown(
                "Level",
                ["All Levels", "Beginner", "Intermediate", "Advanced"],
                FeedState.level_filter,
                FeedState.set_level_filter,
            ),
            filter_dropdown(
                "Time Zone",
                ["All", "Hà Nội", "TP. Hồ Chí Minh", "Online"],
                FeedState.timezone_filter,
                FeedState.set_timezone_filter,
            ),
            filter_dropdown(
                "Availability",
                ["All", "Online", "Offline"],
                rx.cond(FeedState.filter_mode != "", FeedState.filter_mode, "All"),
                FeedState.on_availability_change,
            ),
            rx.vstack(
                rx.text(
                    "Schedule",
                    font_family=FONTS["ui"],
                    font_size="11px",
                    font_weight="600",
                    color=COLORS["text_muted"],
                ),
                rx.button(
                    "Weekly",
                    font_family=FONTS["ui"],
                    font_size="13px",
                    font_weight="700",
                    background_color=COLORS["neon_green"],
                    color="#0b1319",
                    border="none",
                    border_radius="8px",
                    padding="7px 18px",
                    height="38px",
                    cursor="pointer",
                    box_shadow="0 2px 10px rgba(44, 234, 163, 0.3)",
                    _hover={"background_color": "#24d493"},
                ),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.vstack(
                rx.text("Actions", font_size="11px", font_weight="600", color="transparent"),
                rx.button(
                    "+ Post Quest",
                    on_click=FeedState.toggle_create_modal,
                    font_family=FONTS["ui"],
                    font_size="13px",
                    font_weight="700",
                    background_color="rgba(44, 234, 163, 0.12)",
                    color=COLORS["neon_green"],
                    border="1px solid rgba(44, 234, 163, 0.35)",
                    border_radius="8px",
                    padding="7px 16px",
                    height="38px",
                    cursor="pointer",
                    _hover={"background_color": "rgba(44, 234, 163, 0.22)"},
                ),
                spacing="1",
                align="start",
            ),
            spacing="3",
            align="center",
            width="100%",
            wrap="wrap",
        ),
        padding="14px 18px",
        border_radius="14px",
        background_color="rgba(19, 34, 42, 0.6)",
        border="1px solid rgba(255, 255, 255, 0.06)",
        width="100%",
        margin_bottom="16px",
    )
