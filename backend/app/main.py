import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import Base, engine
import app.models  # Nạp toàn bộ models để Base.metadata nhận diện các bảng
from app.routers import (
    auth_router,
    friend_router,
    message_router,
    post_router,
    rating_router,
    room_router,
    upload_router,
    user_router,
    websocket_router,
)
from app.utils.dependencies import limiter


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Khởi tạo bảng tự động khi start server (tiện cho đồ án không cần Docker)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Đảm bảo thư mục upload tồn tại
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield
    await engine.dispose()


app = FastAPI(
    title="ForFriend API",
    description="Nền tảng kết nối tìm bạn học nhóm sinh viên (Online Video Call & Offline Feed)",
    version="0.1.0",
    lifespan=lifespan,
)

# Cấu hình SlowAPI rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Cấu hình CORS cho phép Reflex Frontend giao tiếp
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount thư mục Static Files phục vụ ảnh thẻ và CV
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount các routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(upload_router)
app.include_router(post_router)
app.include_router(room_router)
app.include_router(websocket_router)
app.include_router(rating_router)
app.include_router(friend_router)
app.include_router(message_router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "ForFriend API",
        "version": "0.1.0",
        "docs_url": "/docs",
        "health_check": "/health",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
        "database": "sqlite",
    }
