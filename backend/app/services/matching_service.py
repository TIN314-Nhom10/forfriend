import math
from datetime import datetime, timezone
from typing import List, Tuple
from app.models.post import Post
from app.models.room import Room
from app.models.user import User


class MatchingService:
    """Service tính relevance score giữa user và bài đăng/phòng học."""

    # Hệ thống trọng số chuẩn
    W_SAME_SCHOOL = 3.0      # 40%
    W_SAME_AREA = 2.0        # 30%
    W_SUBJECT_OVERLAP = 2.5  # 30%
    W_RECENCY = 1.0          # Độ tươi mới
    W_AUTHOR_RATING = 1.5    # Điểm đánh giá của tác giả

    def calculate_post_score(self, user: User, post: Post) -> float:
        """
        Tính relevance score giữa user hiện tại và 1 bài đăng (Quest).
        Score = w1 * same_school + w2 * same_area + w3 * subject_overlap 
              + w4 * recency_decay + w5 * author_rating_norm
        """
        score = 0.0

        # 1. Cùng trường (Same school)
        if user.school and post.author and post.author.school:
            if user.school.lower().strip() == post.author.school.lower().strip():
                score += self.W_SAME_SCHOOL

        # 2. Cùng khu vực (Same area: 70% city, 30% district)
        if user.city and post.author and post.author.city:
            if user.city.lower().strip() == post.author.city.lower().strip():
                score += self.W_SAME_AREA * 0.7
                if user.district and post.author.district:
                    if user.district.lower().strip() == post.author.district.lower().strip():
                        score += self.W_SAME_AREA * 0.3

        # 3. Trùng khớp môn học (Jaccard similarity)
        user_subjects = {
            s.subject_name.lower().strip() for s in getattr(user, "subjects", [])
        }
        post_tags = {
            t.tag_name.lower().strip() for t in getattr(post, "tags", [])
        }
        if user_subjects and post_tags:
            intersection = user_subjects & post_tags
            union = user_subjects | post_tags
            overlap = len(intersection) / len(union) if union else 0.0
            score += self.W_SUBJECT_OVERLAP * overlap

        # 4. Suy giảm theo thời gian (Exponential Recency Decay, half-life = 24h)
        post_created = post.created_at
        now = datetime.now(timezone.utc)
        if post_created.tzinfo is None:
            post_created = post_created.replace(tzinfo=timezone.utc)
        age_hours = max(0.0, (now - post_created).total_seconds() / 3600.0)
        recency = math.exp(-0.029 * age_hours)  # ln(2)/24 ≈ 0.02888
        score += self.W_RECENCY * recency

        # 5. Điểm uy tín của tác giả chuẩn hóa (0.0 - 1.0)
        if post.author and post.author.total_ratings > 0:
            rating_norm = min(1.0, max(0.0, post.author.avg_rating / 5.0))
            score += self.W_AUTHOR_RATING * rating_norm

        return round(score, 2)

    def rank_posts(self, user: User, posts: List[Post]) -> List[Tuple[Post, float]]:
        """Rank danh sách bài đăng theo relevance score giảm dần."""
        scored = [(post, self.calculate_post_score(user, post)) for post in posts]
        scored.sort(key=lambda x: (x[1], x[0].created_at), reverse=True)
        return scored

    def calculate_room_score(self, user: User, room: Room) -> float:
        """Tính relevance score giữa user và 1 phòng học trực tuyến."""
        score = 0.0

        # Cùng trường với Host
        if user.school and room.host and room.host.school:
            if user.school.lower().strip() == room.host.school.lower().strip():
                score += self.W_SAME_SCHOOL

        # Cùng thành phố với Host
        if user.city and room.host and room.host.city:
            if user.city.lower().strip() == room.host.city.lower().strip():
                score += self.W_SAME_AREA

        # Chủ đề phòng khớp với môn học quan tâm của User
        user_subjects = {
            s.subject_name.lower().strip() for s in getattr(user, "subjects", [])
        }
        room_topic_lower = room.topic.lower()
        topic_match = any(subj in room_topic_lower for subj in user_subjects) if user_subjects else False
        if topic_match:
            score += self.W_SUBJECT_OVERLAP

        # Recency decay
        room_created = room.created_at
        now = datetime.now(timezone.utc)
        if room_created.tzinfo is None:
            room_created = room_created.replace(tzinfo=timezone.utc)
        age_hours = max(0.0, (now - room_created).total_seconds() / 3600.0)
        recency = math.exp(-0.029 * age_hours)
        score += self.W_RECENCY * recency

        # Host rating
        if room.host and room.host.total_ratings > 0:
            rating_norm = min(1.0, max(0.0, room.host.avg_rating / 5.0))
            score += self.W_AUTHOR_RATING * rating_norm

        return round(score, 2)

    def rank_rooms(self, user: User, rooms: List[Room]) -> List[Tuple[Room, float]]:
        """Rank danh sách phòng học theo relevance score giảm dần."""
        scored = [(room, self.calculate_room_score(user, room)) for room in rooms]
        scored.sort(key=lambda x: (x[1], x[0].created_at), reverse=True)
        return scored


matching_service = MatchingService()
