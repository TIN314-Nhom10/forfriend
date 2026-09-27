import os
import reflex as rx

# LAN IP address of host machine (Wi-Fi: 192.168.1.5)
# Set LAN_IP environment variable if running on a different network IP
LAN_IP = os.getenv("LAN_IP", "192.168.1.122")
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


