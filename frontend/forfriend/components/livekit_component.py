"""
Reflex Custom Component bridge: Bọc thư viện @livekit/components-react
Đây là ngoại lệ JavaScript duy nhất (~5%) trong toàn bộ dự án ForFriend.
Toàn bộ logic, state và điều khiển còn lại đều viết bằng Python thuần.
"""
from typing import Optional
import reflex as rx


class LiveKitRoom(rx.Component):
    """Reflex Custom Component wrap @livekit/components-react LiveKitRoom."""

    library = "@livekit/components-react"
    tag = "LiveKitRoom"

    server_url: rx.Var[str]
    token: rx.Var[str]
    connect: rx.Var[bool] = True
    audio: rx.Var[bool] = True
    video: rx.Var[bool] = True
    screen: rx.Var[bool] = False
    data_lk_theme: rx.Var[str] = "default"


class VideoConference(rx.Component):
    """Grid layout hiển thị luồng video và webcam của các thành viên trong phòng."""

    library = "@livekit/components-react"
    tag = "VideoConference"


class RoomAudioRenderer(rx.Component):
    """Audio renderer cho phép nghe âm thanh từ các thành viên khác qua WebRTC."""

    library = "@livekit/components-react"
    tag = "RoomAudioRenderer"


class ControlBar(rx.Component):
    """Thanh điều khiển WebRTC có sẵn (Mic, Camera, Share Screen, Leave Room)."""

    library = "@livekit/components-react"
    tag = "ControlBar"

    variation: rx.Var[str] = "minimal"


class PreJoin(rx.Component):
    """Giao diện kiểm tra Mic & Camera trước khi vào phòng học."""

    library = "@livekit/components-react"
    tag = "PreJoin"
