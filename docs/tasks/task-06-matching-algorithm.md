# Task 06 — Matching Algorithm

## Mục tiêu
Xây dựng thuật toán đẩy bài đăng/phòng phù hợp tới user dựa trên điểm tương đồng (Relevance Score). Tích hợp vào feed API đã có từ Task 05.

## Phụ thuộc
- Task 05 (Post Feed) — cần modify `get_feed()`
- Task 02 (Models) — cần `User`, `UserSubject`, `Post`, `PostTag`

## Tham chiếu
- [01-architecture.md](../01-architecture.md) — Section 5 (Matching Algorithm)

## Yêu cầu chi tiết

### 6.1. Matching Service

Tạo `backend/app/services/matching_service.py`:

```python
class MatchingService:
    """Service tính relevance score giữa user và post/room."""

    # Weights — có thể tune sau
    W_SAME_SCHOOL = 3.0
    W_SAME_AREA = 2.0
    W_SUBJECT_OVERLAP = 2.5
    W_RECENCY = 1.0
    W_AUTHOR_RATING = 1.5

    def calculate_post_score(self, user: User, post: Post) -> float:
        """
        Tính relevance score giữa user hiện tại và 1 bài đăng.
        
        Score = w1 * same_school + w2 * same_area + w3 * subject_overlap 
              + w4 * recency_decay + w5 * author_rating_norm
        """
        score = 0.0

        # 1. Same school (binary: 0 or 1)
        if user.school.lower().strip() == post.author.school.lower().strip():
            score += self.W_SAME_SCHOOL

        # 2. Same area (compare city + district)
        if user.city.lower().strip() == post.author.city.lower().strip():
            score += self.W_SAME_AREA * 0.7
            if user.district and post.author.district:
                if user.district.lower().strip() == post.author.district.lower().strip():
                    score += self.W_SAME_AREA * 0.3

        # 3. Subject overlap (Jaccard similarity)
        user_subjects = {s.subject_name.lower() for s in user.subjects}
        post_tags = {t.tag_name.lower() for t in post.tags}
        if user_subjects and post_tags:
            intersection = user_subjects & post_tags
            union = user_subjects | post_tags
            overlap = len(intersection) / len(union) if union else 0
            score += self.W_SUBJECT_OVERLAP * overlap

        # 4. Recency decay (exponential decay, half-life = 24h)
        age_hours = (datetime.utcnow() - post.created_at).total_seconds() / 3600
        recency = math.exp(-0.029 * age_hours)  # ln(2)/24 ≈ 0.029
        score += self.W_RECENCY * recency

        # 5. Author rating normalized (0–1)
        if post.author.total_ratings > 0:
            rating_norm = post.author.avg_rating / 5.0
            score += self.W_AUTHOR_RATING * rating_norm

        return round(score, 2)

    def rank_posts(self, user: User, posts: list[Post]) -> list[tuple[Post, float]]:
        """Rank danh sách posts theo relevance score."""
        scored = [(post, self.calculate_post_score(user, post)) for post in posts]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def calculate_room_score(self, user: User, room: Room) -> float:
        """Tính relevance score giữa user và 1 room (tương tự post)."""
        score = 0.0

        # Same school as host
        if user.school.lower().strip() == room.host.school.lower().strip():
            score += self.W_SAME_SCHOOL

        # Same area as host
        if user.city.lower().strip() == room.host.city.lower().strip():
            score += self.W_SAME_AREA

        # Topic match with user subjects
        user_subjects = {s.subject_name.lower() for s in user.subjects}
        room_topic_lower = room.topic.lower()
        topic_match = any(subj in room_topic_lower for subj in user_subjects)
        if topic_match:
            score += self.W_SUBJECT_OVERLAP

        # Recency
        age_hours = (datetime.utcnow() - room.created_at).total_seconds() / 3600
        recency = math.exp(-0.029 * age_hours)
        score += self.W_RECENCY * recency

        # Host rating
        if room.host.total_ratings > 0:
            score += self.W_AUTHOR_RATING * (room.host.avg_rating / 5.0)

        return round(score, 2)
```

### 6.2. Tích hợp vào Feed API

Modify `PostService.get_feed()`:
1. Query tất cả active posts (đã filter + phân trang ban đầu lấy rộng hơn)
2. Gọi `MatchingService.rank_posts(user, posts)` 
3. Apply score rồi phân trang chính xác
4. Set `relevance_score` vào response

**Chiến lược phân trang với scoring:**
- Lấy nhiều hơn cần thiết (ví dụ: 100 bài gần nhất)
- Score + sort ở application layer
- Trả đúng `per_page` bài theo thứ tự score

### 6.3. Caching (In-Memory Python với TTL)

Để không phụ thuộc vào server Redis bên ngoài, hệ thống sử dụng cache in-memory viết bằng Python thuần trong `backend/app/utils/memory_cache.py`:

```python
import time
from typing import Any

class InMemoryCache:
    """Quản lý cache trong RAM sử dụng Python dictionary có cơ chế hết hạn (TTL)."""
    
    def __init__(self):
        # Lưu trữ: { key: (expires_at, value) }
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        """Lấy giá trị từ cache, trả về None nếu không tồn tại hoặc đã hết hạn."""
        if key not in self._store:
            return None
        expires_at, value = self._store[key]
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """Lưu giá trị vào cache với TTL (mặc định 5 phút = 300s)."""
        expires_at = time.time() + ttl_seconds
        self._store[key] = (expires_at, value)

    def delete(self, key: str) -> None:
        """Xóa 1 key cụ thể."""
        self._store.pop(key, None)

    def invalidate_prefix(self, prefix: str) -> None:
        """Xóa toàn bộ key bắt đầu bằng prefix (ví dụ khi có post mới)."""
        keys_to_delete = [k for k in self._store.keys() if k.startswith(prefix)]
        for k in keys_to_delete:
            del self._store[k]

feed_cache = InMemoryCache()
```

- Cache feed kết quả cho mỗi user, TTL = 5 phút (300 giây).
- Cache key: `feed:{user_id}:{page}:{per_page}:{filters_hash}`.
- Invalidate khi:
  - User tạo post mới → `feed_cache.invalidate_prefix("feed:")`
  - User update profile (school, subjects thay đổi) → xóa cache tương ứng

### 6.4. Tích hợp vào Room Lobby

Modify `RoomService.get_rooms()`:
- Tương tự feed: rank rooms theo relevance score
- Phòng score cao hiển thị trước trong lobby

### 6.5. Tests

- Test score = 0 khi user và author hoàn toàn khác nhau
- Test score tăng khi cùng school
- Test score tăng khi cùng area
- Test subject overlap tính đúng Jaccard
- Test recency decay: bài cũ hơn → score thấp hơn
- Test author rating ảnh hưởng score
- Test ranking order đúng
- Test in-memory cache hit/miss và kiểm tra TTL

## Tiêu chí hoàn thành

- [ ] MatchingService tính score đúng theo công thức
- [ ] Feed API trả posts sắp xếp theo relevance_score
- [ ] Room lobby sắp xếp theo relevance_score  
- [ ] In-Memory cache hoạt động ổn định (TTL 5 phút, 0% Redis)
- [ ] Invalidate cache tự động khi có bài đăng mới
- [ ] `relevance_score` field có trong response
- [ ] Tests pass cho tất cả test cases
