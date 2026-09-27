"""Profile Page: Hồ sơ Hero, Đổi Avatar trong 15 Chibi, Upload thẻ SV & CV, và Lịch sử đánh giá với Glassmorphism."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.common import pixel_title, avatar_display, star_rating, game_card, game_button, game_input
from ..components.layout.game_layout import game_layout
from ..state.profile_state import ProfileState
from ..state.base_state import BaseState
from ..state.models import ReviewItem

STUDENT_AVATARS = [
    (1, "Alex"), (2, "Sophia"), (3, "Daniel"), (4, "Emma"), (5, "Lucas"),
    (6, "Mia"), (7, "Ethan"), (8, "Olivia"), (9, "James"), (10, "Isabella"),
    (11, "Benjamin"), (12, "Charlotte"), (13, "Henry"), (14, "Amelia"), (15, "Leo"),
]


def avatar_change_item(char_info: tuple[int, str]) -> rx.Component:
    """Từng ô đổi avatar trong hồ sơ với viền phát sáng khi chọn."""
    char_id, class_name = char_info
    is_cur = ProfileState.profile_data["avatar_id"] == char_id

    return rx.box(
        rx.vstack(
            rx.image(
                src=f"/avatars/avatar_{char_id}.png",
                width="48px",
                height="48px",
                border_radius="50%",
                object_fit="cover",
            ),
            rx.text(
                class_name,
                font_family=FONTS["ui"],
                font_size="11px",
                font_weight="700",
                color=rx.cond(is_cur, COLORS["neon_green"], COLORS["text_secondary"]),
            ),
            spacing="1",
            align="center",
        ),
        on_click=ProfileState.change_avatar(char_id),
        padding="8px 6px",
        border_radius="10px",
        cursor="pointer",
        background_color=rx.cond(is_cur, "rgba(0, 255, 136, 0.12)", "rgba(255, 255, 255, 0.03)"),
        border=rx.cond(is_cur, f"2px solid {COLORS['neon_green']}", "1px solid rgba(255, 255, 255, 0.08)"),
        box_shadow=rx.cond(is_cur, "0 0 14px rgba(0, 255, 136, 0.35)", "none"),
        transition="all 200ms ease",
        _hover={
            "border_color": COLORS["neon_green"],
            "transform": "scale(1.06)",
        },
    )


def review_history_row(rev: ReviewItem) -> rx.Component:
    """Từng dòng nhận xét từ bạn học."""
    return rx.hstack(
        avatar_display(rev.reviewer_avatar_id, size="40px"),
        rx.vstack(
            rx.hstack(
                rx.text(rev.reviewer_name, font_family=FONTS["ui"], font_weight="700", color=COLORS["text_main"], font_size="14px"),
                rx.text(rx.hstack(rx.text("• "), rx.text(rev.created_at)), color=COLORS["text_muted"], font_size="12px"),
                star_rating(rev.stars),
                spacing="2",
                align="center",
            ),
            rx.text(
                rx.hstack(rx.text('"'), rx.text(rev.comment), rx.text('"')),
                font_size="13px",
                color="#cbd5e1",
                font_style="italic",
            ),
            spacing="1",
            align="start",
        ),
        spacing="3",
        align="center",
        padding="12px 16px",
        background_color="rgba(255, 255, 255, 0.03)",
        border="1px solid rgba(255, 255, 255, 0.06)",
        border_radius="10px",
        width="100%",
    )


def profile_page() -> rx.Component:
    """Giao diện Hồ sơ Hero."""
    return game_layout(
        rx.vstack(
            # Hero Header Banner
            game_card(
                rx.hstack(
                    avatar_display(ProfileState.profile_data["avatar_id"], size="76px"),
                    rx.vstack(
                        rx.hstack(
                            pixel_title(ProfileState.profile_data["name"], size="22px", color=COLORS["neon_green"]),
                            rx.cond(
                                ProfileState.profile_data["is_verified"],
                                rx.badge(
                                    "VERIFIED STUDENT ✓",
                                    bg="rgba(0, 255, 136, 0.15)",
                                    color=COLORS["neon_green"],
                                    border="1px solid rgba(0, 255, 136, 0.4)",
                                    font_family=FONTS["ui"],
                                    font_size="11px",
                                    font_weight="700",
                                    padding="3px 10px",
                                    border_radius="9999px",
                                ),
                                rx.badge(
                                    "UNVERIFIED",
                                    bg="rgba(255, 255, 255, 0.05)",
                                    color=COLORS["text_muted"],
                                    font_family=FONTS["ui"],
                                    font_size="11px",
                                    font_weight="600",
                                    padding="3px 10px",
                                    border_radius="9999px",
                                ),
                            ),
                            spacing="3",
                            align="center",
                        ),
                        rx.text(f"Email: {ProfileState.profile_data['email']}", font_family=FONTS["ui"], color=COLORS["text_muted"], font_size="13px"),
                        rx.hstack(
                            star_rating(ProfileState.profile_data["avg_rating"]),
                            rx.text(
                                f"({ProfileState.profile_data['total_ratings']} reviews)",
                                font_family=FONTS["ui"],
                                font_size="12px",
                                color=COLORS["text_muted"],
                            ),
                            spacing="2",
                            align="center",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    game_button(
                        rx.cond(
                            ProfileState.is_editing,
                            "✕ Cancel",
                            "✎ Edit Profile",
                        ),
                        on_click=ProfileState.toggle_edit,
                        variant="secondary",
                        style={"font_size": "13px", "padding": "8px 18px"},
                    ),
                    width="100%",
                    align="center",
                    wrap="wrap",
                ),
                width="100%",
            ),
            # Edit Form (If editing)
            rx.cond(
                ProfileState.is_editing,
                game_card(
                    rx.vstack(
                        pixel_title(
                            "EDIT PROFILE",
                            size="16px",
                            color=COLORS["neon_cyan"],
                        ),
                        rx.text(
                            "Full Name:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input("Name", ProfileState.edit_name, ProfileState.set_edit_name),
                        rx.text(
                            "Bio / About Me:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        rx.text_area(
                            value=ProfileState.edit_bio,
                            on_change=ProfileState.set_edit_bio,
                            background_color="rgba(10, 10, 24, 0.8)",
                            border="1px solid rgba(255, 255, 255, 0.1)",
                            border_radius="8px",
                            color=COLORS["text_main"],
                            font_family=FONTS["body"],
                            font_size="14px",
                            padding="12px",
                            width="100%",
                        ),
                        rx.text(
                            "University:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input("University", ProfileState.edit_school, ProfileState.set_edit_school),
                        rx.text(
                            "City:",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input("City", ProfileState.edit_city, ProfileState.set_edit_city),
                        rx.text(
                            "Interested Subjects (comma separated):",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            font_weight="700",
                            color=COLORS["neon_cyan"],
                        ),
                        game_input("Subjects", ProfileState.edit_subjects_input, ProfileState.set_edit_subjects_input),
                        game_button(
                            "💾 Save Changes",
                            on_click=ProfileState.save_profile,
                            variant="primary",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            # Avatar Selector Section
            game_card(
                rx.vstack(
                    pixel_title(
                        "★ AVATAR ROSTER (15 STYLES) ★",
                        size="15px",
                        color=COLORS["neon_pink"],
                    ),
                    rx.text(
                        "Click an avatar to change your profile picture:",
                        font_family=FONTS["ui"],
                        font_size="13px",
                        color=COLORS["text_muted"],
                    ),
                    rx.grid(
                        *[avatar_change_item(c) for c in STUDENT_AVATARS],
                        columns=rx.breakpoints(initial="3", sm="5", md="8"),
                        spacing="3",
                        width="100%",
                        padding_y="6px",
                    ),
                    spacing="3",
                    width="100%",
                ),
                width="100%",
            ),
            # Document Verification & CV Uploads
            rx.hstack(
                # Student ID Card Upload
                game_card(
                    rx.vstack(
                        pixel_title(
                            "🎓 STUDENT ID VERIFICATION",
                            size="15px",
                            color=COLORS["neon_cyan"],
                        ),
                        rx.text(
                            "Upload student ID card (JPG/PNG <= 5MB) for Verified badge.",
                            font_family=FONTS["ui"],
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        rx.upload(
                            rx.center(
                                rx.vstack(
                                    rx.text("📁", font_size="22px"),
                                    rx.text(
                                        "Drag & drop image or click to upload ID",
                                        font_family=FONTS["ui"],
                                        font_size="12px",
                                        font_weight="600",
                                        color=COLORS["neon_green"],
                                    ),
                                    spacing="1",
                                    align="center",
                                ),
                                height="90px",
                                border=f"2px dashed rgba(0, 255, 136, 0.4)",
                                border_radius="10px",
                                background="rgba(0, 255, 136, 0.03)",
                                width="100%",
                            ),
                            id="upload_student_id",
                            accept={"image/*": [".png", ".jpg", ".jpeg"]},
                            max_files=1,
                        ),
                        game_button(
                            "Upload Student ID",
                            on_click=ProfileState.handle_student_id_upload(rx.upload_files(upload_id="upload_student_id")),
                            variant="secondary",
                            style={"font_size": "12px", "width": "100%"},
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    flex="1",
                ),
                # CV Upload
                game_card(
                    rx.vstack(
                        pixel_title(
                            "📄 STUDENT RESUME (CV)",
                            size="15px",
                            color=COLORS["neon_gold"],
                        ),
                        rx.text(
                            "Upload student CV (PDF <= 10MB) to showcase skills to allies.",
                            font_family=FONTS["ui"],
                            font_size="12px",
                            color=COLORS["text_muted"],
                        ),
                        rx.upload(
                            rx.center(
                                rx.vstack(
                                    rx.text("📄", font_size="22px"),
                                    rx.text(
                                        "Drag & drop PDF or click to upload CV",
                                        font_family=FONTS["ui"],
                                        font_size="12px",
                                        font_weight="600",
                                        color=COLORS["neon_gold"],
                                    ),
                                    spacing="1",
                                    align="center",
                                ),
                                height="90px",
                                border=f"2px dashed rgba(255, 230, 0, 0.4)",
                                border_radius="10px",
                                background="rgba(255, 230, 0, 0.03)",
                                width="100%",
                            ),
                            id="upload_cv",
                            accept={"application/pdf": [".pdf"]},
                            max_files=1,
                        ),
                        game_button(
                            "Upload CV PDF",
                            on_click=ProfileState.handle_cv_upload(rx.upload_files(upload_id="upload_cv")),
                            variant="secondary",
                            style={"font_size": "12px", "width": "100%", "color": COLORS["neon_gold"], "border_color": "rgba(255, 230, 0, 0.4)"},
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    flex="1",
                ),
                spacing="4",
                width="100%",
                wrap="wrap",
            ),
            # Reviews Received Section
            game_card(
                rx.vstack(
                    pixel_title(
                        "★ REVIEWS FROM ALLIES ★",
                        size="15px",
                        color=COLORS["neon_gold"],
                    ),
                    rx.cond(
                        ProfileState.ratings_history.length() == 0,
                        rx.text(
                            "No reviews yet. Join study rooms to earn reputations!",
                            font_family=FONTS["ui"],
                            font_size="13px",
                            color=COLORS["text_muted"],
                        ),
                        rx.vstack(
                            rx.foreach(ProfileState.ratings_history, review_history_row),
                            spacing="2",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                width="100%",
            ),
            spacing="5",
            width="100%",
        ),
        on_mount=ProfileState.load_profile,
    )
