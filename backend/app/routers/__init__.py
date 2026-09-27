"""FastAPI API Routers."""
from app.routers.auth import router as auth_router
from app.routers.friend import router as friend_router
from app.routers.message import router as message_router
from app.routers.post import router as post_router
from app.routers.rating import router as rating_router
from app.routers.room import router as room_router
from app.routers.upload import router as upload_router
from app.routers.user import router as user_router
from app.routers.websocket import router as websocket_router

__all__ = [
    "auth_router",
    "user_router",
    "upload_router",
    "post_router",
    "room_router",
    "websocket_router",
    "rating_router",
    "friend_router",
    "message_router",
]

