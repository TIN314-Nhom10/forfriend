"""Video Call Room Page: Phòng học ảo tích hợp LiveKit WebRTC với Modern Glassmorphism."""
import reflex as rx
from ..styles.theme import COLORS, FONTS
from ..components.common import pixel_title, game_button, toast_banner
from ..components.livekit_component import LiveKitRoom, VideoConference, RoomAudioRenderer, ControlBar
from ..components.room.request_approval_modal import request_approval_modal
from ..components.rating.rating_modal import rating_modal
from ..state.room_state import RoomState


def video_call_page() -> rx.Component:
    """Giao diện phòng học ảo và hội nghị video WebRTC phong cách Cyberpunk."""
    return rx.box(
        toast_banner(),
        request_approval_modal(),
        rating_modal(),
        rx.vstack(
            # Top Control Bar
            rx.hstack(
                rx.hstack(
                    rx.box(
                        width="10px",
                        height="10px",
                        border_radius="50%",
                        background_color="#ff4d6d",
                        box_shadow="0 0 10px #ff4d6d",
                        class_name="pulse-dot",
                    ),
                    pixel_title("ONLINE STUDY ROOM", size="16px", color=COLORS["neon_green"]),
                    rx.badge(
                        "LIVEKIT WEBRTC",
                        bg="rgba(0, 255, 136, 0.12)",
                        color=COLORS["neon_green"],
                        border="1px solid rgba(0, 255, 136, 0.3)",
                        font_family=FONTS["ui"],
                        font_size="10px",
                        font_weight="700",
                        padding="2px 8px",
                        border_radius="6px",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.spacer(),
                # Host Controls
                rx.cond(
                    RoomState.is_host,
                    game_button(
                        "🚪 Knock Requests",
                        on_click=RoomState.toggle_approval_modal,
                        variant="pink",
                        style={"font_size": "12px", "padding": "6px 14px"},
                    ),
                ),
                # Leave Button
                game_button(
                    "Leave Room ✕",
                    on_click=RoomState.leave_room,
                    variant="ghost",
                    style={
                        "font_size": "12px",
                        "padding": "6px 14px",
                        "color": COLORS["danger"],
                        "border_color": "rgba(255, 77, 109, 0.4)",
                        "_hover": {"background": "rgba(255, 77, 109, 0.15)", "border_color": COLORS["danger"]},
                    },
                ),
                padding="14px 24px",
                background_color="rgba(14, 14, 30, 0.85)",
                backdrop_filter="blur(16px)",
                border_bottom="1px solid rgba(255, 255, 255, 0.08)",
                width="100%",
                align="center",
            ),
            # LiveKit Video Conference Container
            rx.box(
                rx.cond(
                    RoomState.livekit_token != "",
                    LiveKitRoom.create(
                        VideoConference.create(),
                        RoomAudioRenderer.create(),
                        ControlBar.create(),
                        server_url=RoomState.livekit_url,
                        token=RoomState.livekit_token,
                        connect=True,
                        audio=True,
                        video=True,
                    ),
                    rx.center(
                        rx.vstack(
                            rx.spinner(color=COLORS["neon_green"], size="3"),
                            rx.text("Connecting WebRTC LiveKit Cloud...", font_family=FONTS["ui"], font_size="14px", font_weight="600", color=COLORS["neon_green"]),
                            rx.text("If not approved yet, please wait for Host to accept knock request.", font_family=FONTS["ui"], font_size="13px", color=COLORS["text_muted"]),
                            spacing="3",
                            align="center",
                        ),
                        height="80vh",
                        width="100%",
                    ),
                ),
                flex="1",
                width="100%",
                height="calc(100vh - 60px)",
                background_color="transparent",
            ),
            spacing="0",
            width="100%",
            height="100vh",
        ),
        background_color=COLORS["bg_dark"],
        height="100vh",
        width="100%",
        on_mount=RoomState.on_video_call_mount,
    )
