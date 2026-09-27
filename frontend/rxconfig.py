import os
import socket
import reflex as rx


def get_local_ip() -> str:
    """Auto-detect the host machine's primary local IP address."""
    env_ip = os.getenv("LAN_IP")
    if env_ip:
        return env_ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Connect to public DNS to determine active outbound interface IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


LAN_IP = get_local_ip()
API_URL = os.getenv("REFLEX_API_URL", f"http://{LAN_IP}:8001")

config = rx.Config(
    app_name="forfriend",
    backend_host="0.0.0.0",
    backend_port=8001,
    frontend_port=3000,
    api_url=API_URL,
    cors_allowed_origins=["*"],
    plugins=[
        rx.plugins.SitemapPlugin(trailing_slash="preserve"),
        rx.plugins.RadixThemesPlugin(),
    ],
)


