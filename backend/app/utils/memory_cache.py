import time
from typing import Any, Dict, Optional, Tuple


class MemoryCache:
    """
    In-Memory Cache thuần Python có hỗ trợ TTL (Time-To-Live).
    Thay thế hoàn toàn Redis cho việc lưu trữ session/matching cache.
    """

    def __init__(self) -> None:
        # Lưu trữ: key -> (value, expire_timestamp | None)
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Lưu một giá trị vào cache kèm TTL tùy chọn (tính bằng giây)."""
        expire_at = (time.time() + ttl_seconds) if ttl_seconds is not None else None
        self._store[key] = (value, expire_at)

    def get(self, key: str, default: Any = None) -> Any:
        """Lấy giá trị từ cache. Nếu đã hết hạn sẽ tự động xóa và trả về default."""
        if key not in self._store:
            return default

        value, expire_at = self._store[key]
        if expire_at is not None and time.time() > expire_at:
            del self._store[key]
            return default

        return value

    def delete(self, key: str) -> bool:
        """Xóa một key khỏi cache. Trả về True nếu key tồn tại."""
        if key in self._store:
            del self._store[key]
            return True
        return False

    def has(self, key: str) -> bool:
        """Kiểm tra key có tồn tại và còn hạn không."""
        return self.get(key) is not None

    def clear(self) -> None:
        """Xóa toàn bộ cache."""
        self._store.clear()

    def cleanup_expired(self) -> int:
        """Dọn dẹp các key đã hết hạn để giải phóng RAM. Trả về số key đã dọn."""
        now = time.time()
        expired_keys = [
            k for k, (_, exp) in self._store.items() if exp is not None and now > exp
        ]
        for k in expired_keys:
            del self._store[k]
        return len(expired_keys)

    def invalidate_prefix(self, prefix: str) -> int:
        """Xóa toàn bộ các key bắt đầu bằng prefix (ví dụ 'feed:'). Trả về số key đã xóa."""
        keys_to_delete = [k for k in self._store.keys() if k.startswith(prefix)]
        for k in keys_to_delete:
            del self._store[k]
        return len(keys_to_delete)


# Singleton cache instance dùng chung cho ứng dụng
cache = MemoryCache()
memory_cache = cache
