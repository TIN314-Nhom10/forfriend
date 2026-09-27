import json
import logging
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from jose import JWTError

from app.database import AsyncSessionLocal
from app.models.user import User
from app.services.friend_service import friend_service
from app.services.message_service import message_service
from app.utils.security import decode_token
from app.websockets.connection_manager import chat_manager, notification_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/notifications")
async def ws_notifications(websocket: WebSocket, token: str = Query(...)):
    """
    WebSocket endpoint nhận thông báo real-time qua RAM in-memory.
    Xác thực bằng JWT token truyền qua query param.
    """
    # 1. Xác thực token
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            await websocket.close(code=4001, reason="Invalid token type")
            return
        user_id_str = payload.get("sub")
        if not user_id_str:
            await websocket.close(code=4001, reason="Missing user ID")
            return
        user_uuid = uuid.UUID(user_id_str)
    except (JWTError, ValueError) as e:
        logger.warning(f"WebSocket auth failed: {e}")
        await websocket.close(code=4001, reason="Invalid auth token")
        return

    # 2. Kiểm tra user trong DB
    friend_ids = []
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_uuid)
        if not user or not user.is_active:
            await websocket.close(code=4001, reason="User not found or inactive")
            return

        # 3. Kết nối vào ConnectionManager (In-Memory)
        user_id = str(user.id)
        await notification_manager.connect(websocket, user_id=user_id)
        logger.info(f"WebSocket connected: User {user.name} ({user_id})")

        # Broadcast user_online tới bạn bè
        try:
            friends = await friend_service.get_friends(db, user)
            friend_ids = [str(f.friend.id) for f in friends]
            if friend_ids:
                await notification_manager.broadcast_to_users(
                    friend_ids,
                    {"type": "user_online", "data": {"user_id": user_id, "name": user.name}},
                )
        except Exception as e:
            logger.warning(f"Failed to broadcast user_online: {e}")

    # 4. Giữ kết nối và xử lý ping/pong
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        notification_manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected: User {user_id}")
    except Exception as e:
        notification_manager.disconnect(websocket)
        logger.warning(f"WebSocket error for user {user_id}: {e}")
    finally:
        # Nếu user không còn kết nối nào, broadcast user_offline tới bạn bè
        if not notification_manager.is_user_online(user_id) and friend_ids:
            try:
                await notification_manager.broadcast_to_users(
                    friend_ids,
                    {"type": "user_offline", "data": {"user_id": user_id}},
                )
            except Exception as e:
                logger.warning(f"Failed to broadcast user_offline: {e}")


@router.websocket("/ws/chat/{friend_id}")
async def ws_chat(
    websocket: WebSocket,
    friend_id: uuid.UUID,
    token: str = Query(...),
):
    """
    WebSocket endpoint nhắn tin 1-1 real-time trực tiếp trong RAM.
    Được bảo vệ bởi JWT và kiểm tra quan hệ bạn bè.
    """
    # 1. Xác thực token
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            await websocket.close(code=4001, reason="Invalid token type")
            return
        user_id_str = payload.get("sub")
        if not user_id_str:
            await websocket.close(code=4001, reason="Missing user ID")
            return
        user_uuid = uuid.UUID(user_id_str)
    except (JWTError, ValueError) as e:
        logger.warning(f"WebSocket chat auth failed: {e}")
        await websocket.close(code=4001, reason="Invalid auth token")
        return

    # 2. Kiểm tra user và xác nhận là bạn bè
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_uuid)
        if not user or not user.is_active:
            await websocket.close(code=4001, reason="User not found or inactive")
            return

        are_friends = await friend_service.are_friends(db, user.id, friend_id)
        if not are_friends:
            await websocket.close(code=4003, reason="Not friends")
            return

    # 3. Kết nối vào ChatConnectionManager
    uid_str = str(user.id)
    fid_str = str(friend_id)
    await chat_manager.connect(uid_str, fid_str, websocket)
    logger.info(f"WebSocket chat connected: User {user.name} ({uid_str}) -> Friend {fid_str}")

    # 4. Vòng lặp nhận và điều phối tin nhắn
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")

            if event_type == "message":
                content = data.get("content", "")
                if not content or not content.strip():
                    continue

                async with AsyncSessionLocal() as db:
                    msg = await message_service.create_message(
                        db, user.id, friend_id, content
                    )

                    chat_payload = {
                        "type": "message",
                        "content": msg.content,
                        "message_id": str(msg.id),
                        "sender_id": uid_str,
                        "created_at": msg.created_at.isoformat(),
                    }

                    # Echo về sender
                    await websocket.send_text(
                        json.dumps({**chat_payload, "is_mine": True}, ensure_ascii=False)
                    )

                    # Gửi tới cửa sổ chat của bạn bè nếu đang mở
                    sent_to_chat = await chat_manager.send_to_chat(
                        uid_str, fid_str, {**chat_payload, "is_mine": False}
                    )

                    # Nếu bạn bè không mở khung chat này, gửi toast notification
                    if not sent_to_chat:
                        await notification_manager.send_to_user(
                            fid_str,
                            {
                                "type": "new_message",
                                "data": {
                                    "from": uid_str,
                                    "from_name": user.name,
                                    "from_avatar": user.avatar_id,
                                    "content": msg.content[:100],
                                    "created_at": msg.created_at.isoformat(),
                                },
                            },
                        )

            elif event_type == "typing":
                await chat_manager.send_to_chat(
                    uid_str, fid_str, {"type": "typing", "from": uid_str}
                )

            elif event_type == "stop_typing":
                await chat_manager.send_to_chat(
                    uid_str, fid_str, {"type": "stop_typing", "from": uid_str}
                )

            elif event_type == "read":
                async with AsyncSessionLocal() as db:
                    await message_service.mark_read(db, user.id, friend_id)
                await chat_manager.send_to_chat(
                    uid_str,
                    fid_str,
                    {
                        "type": "read",
                        "read_by": uid_str,
                        "read_at": datetime.now(timezone.utc).isoformat(),
                    },
                )

    except WebSocketDisconnect:
        chat_manager.disconnect(uid_str, fid_str)
        logger.info(f"WebSocket chat disconnected: {uid_str} -> {fid_str}")
    except Exception as e:
        chat_manager.disconnect(uid_str, fid_str)
        logger.warning(f"WebSocket chat error ({uid_str} -> {fid_str}): {e}")

