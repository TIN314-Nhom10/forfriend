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
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "3000"))
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8001"))

# If REFLEX_API_URL is explicitly set, use it.
# Otherwise, in Docker / Render production, default to localhost so client-side browser
# automatically connects to window.location.origin (HTTPS/WSS on the same domain)
# via Reflex's built-in SAME_DOMAIN_HOSTNAMES logic.
env_api_url = os.getenv("REFLEX_API_URL")
if env_api_url:
    API_URL = env_api_url
elif os.getenv("IN_DOCKER") or os.getenv("RENDER"):
    API_URL = f"http://localhost:{BACKEND_PORT}"
else:
    API_URL = f"http://{LAN_IP}:{BACKEND_PORT}"

config_kwargs = {
    "app_name": "forfriend",
    "backend_host": "0.0.0.0",
    "backend_port": BACKEND_PORT,
    "api_url": API_URL,
    "cors_allowed_origins": ["*"],
    "plugins": [
        rx.plugins.SitemapPlugin(trailing_slash="preserve"),
        rx.plugins.RadixThemesPlugin(),
    ],
}

# Only include frontend_port if not in backend-only mode, because Reflex CLI errors
# with 'Cannot specify --frontend-port when not running frontend' if present.
if not os.getenv("REFLEX_BACKEND_ONLY"):
    config_kwargs["frontend_port"] = int(os.getenv("FRONTEND_PORT", "3000"))

config = rx.Config(**config_kwargs)


