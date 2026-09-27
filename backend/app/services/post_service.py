import math
import uuid
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.post import Post, PostTag
from app.models.user import User
from app.schemas.post import (
    AuthorBrief,
    PostCreate,
    PostListResponse,
    PostResponse,
    PostUpdate,
)
from app.services.matching_service import matching_service
from app.utils.memory_cache import cache
from app.utils.security import sanitize_text

FEED_CACHE_TTL = 300  # 5 phút (300 giây)


class PostService:
    """Business Logic Service phụ trách quản lý Bảng tin tìm bạn học (Post Feed & Matching)."""

    @staticmethod
    def _format_post_response(
        post: Post, relevance_score: Optional[float] = None
    ) -> PostResponse:
        author_brief = AuthorBrief(
            id=post.author.id,
            name=post.author.name,
            avatar_id=post.author.avatar_id,
            school=post.author.school,
            avg_rating=post.author.avg_rating,
        )
        tag_names = [t.tag_name for t in post.tags]
        return PostResponse(
            id=post.id,
            content=post.content,
            study_type=post.study_type,
            location=post.location,
            preferred_school=post.preferred_school,
            study_date=post.study_date,
            max_people=post.max_people,
            author=author_brief,
            tags=tag_names,
            relevance_score=relevance_score,
            created_at=post.created_at,
        )

    @staticmethod
    async def create_post(
        db: AsyncSession, author: User, data: PostCreate
    ) -> PostResponse:
        clean_content = sanitize_text(data.content) or data.content
        clean_location = sanitize_text(data.location)
        clean_pref_school = sanitize_text(data.preferred_school)

        post = Post(
            author_id=author.id,
            content=clean_content,
            study_type=data.study_type,
            location=clean_location,
            preferred_school=clean_pref_school,
            study_date=data.study_date,
            max_people=data.max_people,
        )
        db.add(post)
        await db.flush()

        # Thêm các tags liên kết
        clean_tags = set()
        for tag in data.tags:
            tag_name = sanitize_text(tag.lower().strip())
            if tag_name and tag_name not in clean_tags:
                clean_tags.add(tag_name)
                db.add(PostTag(post_id=post.id, tag_name=tag_name))

        await db.commit()

        # Invalidate toàn bộ cache feed khi có bài đăng mới
        cache.invalidate_prefix("feed:")

        # Nạp lại dữ liệu kèm relations
        stmt = (
            select(Post)
            .where(Post.id == post.id)
            .options(selectinload(Post.author), selectinload(Post.tags))
        )
        res = await db.execute(stmt)
        full_post = res.scalar_one()

        return PostService._format_post_response(full_post)

    @staticmethod
    async def get_feed(
        db: AsyncSession,
        user: User,
        page: int = 1,
        per_page: int = 20,
        study_type: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> PostListResponse:
        cache_key = f"feed:{user.id}:{page}:{per_page}:{study_type or ''}:{tag or ''}"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        # Đảm bảo nạp đầy đủ user.subjects để tính matching score
        user_stmt = select(User).where(User.id == user.id).options(selectinload(User.subjects))
        user_res = await db.execute(user_stmt)
        current_user = user_res.scalar_one()

        # Điều kiện lọc bài viết
        conditions = [Post.is_active.is_(True)]

        if study_type:
            conditions.append(Post.study_type == study_type.lower())

        if tag:
            clean_tag = tag.lower().strip()
            conditions.append(Post.tags.any(PostTag.tag_name == clean_tag))

        # Lấy candidate pool (tối đa 100 bài viết gần nhất thỏa mãn bộ lọc)
        fetch_stmt = (
            select(Post)
            .where(*conditions)
            .options(selectinload(Post.author), selectinload(Post.tags))
            .order_by(Post.created_at.desc())
            .limit(100)
        )
        fetch_res = await db.execute(fetch_stmt)
        candidate_posts = fetch_res.scalars().all()

        # Áp dụng thuật toán Matching Ranking
        ranked_pairs = matching_service.rank_posts(current_user, list(candidate_posts))

        total = len(ranked_pairs)
        offset = (page - 1) * per_page
        paged_pairs = ranked_pairs[offset : offset + per_page]

        items = [
            PostService._format_post_response(post, relevance_score=score)
            for post, score in paged_pairs
        ]
        total_pages = math.ceil(total / per_page) if total > 0 else 1

        response = PostListResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

        # Lưu kết quả vào In-Memory Cache (TTL 5 phút)
        cache.set(cache_key, response, ttl_seconds=FEED_CACHE_TTL)
        return response

    @staticmethod
    async def get_post(db: AsyncSession, post_id: uuid.UUID) -> PostResponse:
        stmt = (
            select(Post)
            .where(Post.id == post_id, Post.is_active.is_(True))
            .options(selectinload(Post.author), selectinload(Post.tags))
        )
        res = await db.execute(stmt)
        post = res.scalar_one_or_none()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bài đăng hoặc bài viết đã bị xóa",
            )

        return PostService._format_post_response(post)

    @staticmethod
    async def update_post(
        db: AsyncSession, user_id: uuid.UUID, post_id: uuid.UUID, data: PostUpdate
    ) -> PostResponse:
        stmt = (
            select(Post)
            .where(Post.id == post_id, Post.is_active.is_(True))
            .options(selectinload(Post.author), selectinload(Post.tags))
        )
        res = await db.execute(stmt)
        post = res.scalar_one_or_none()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bài đăng",
            )

        # Kiểm tra quyền: Chỉ tác giả bài đăng mới được chỉnh sửa
        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền chỉnh sửa bài đăng của người khác",
            )

        if data.content is not None:
            post.content = sanitize_text(data.content) or data.content
        if data.study_type is not None:
            post.study_type = data.study_type
        if data.location is not None:
            post.location = sanitize_text(data.location)
        if data.preferred_school is not None:
            post.preferred_school = sanitize_text(data.preferred_school)
        if data.study_date is not None:
            post.study_date = data.study_date
        if data.max_people is not None:
            post.max_people = data.max_people

        # Cập nhật tags nếu được truyền
        if data.tags is not None:
            await db.execute(delete(PostTag).where(PostTag.post_id == post.id))
            clean_tags = set()
            for tag in data.tags:
                tag_name = sanitize_text(tag.lower().strip())
                if tag_name and tag_name not in clean_tags:
                    clean_tags.add(tag_name)
                    db.add(PostTag(post_id=post.id, tag_name=tag_name))

        await db.commit()

        # Invalidate cache feed
        cache.invalidate_prefix("feed:")

        # Nạp lại bản ghi
        res = await db.execute(stmt)
        updated_post = res.scalar_one()

        return PostService._format_post_response(updated_post)

    @staticmethod
    async def delete_post(
        db: AsyncSession, user_id: uuid.UUID, post_id: uuid.UUID
    ) -> None:
        stmt = select(Post).where(Post.id == post_id, Post.is_active.is_(True))
        res = await db.execute(stmt)
        post = res.scalar_one_or_none()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy bài đăng",
            )

        # Kiểm tra quyền: Chỉ tác giả bài đăng mới được xóa
        if post.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền xóa bài đăng của người khác",
            )

        # Soft delete: Cập nhật cờ is_active = False
        post.is_active = False
        await db.commit()

        # Invalidate cache feed
        cache.invalidate_prefix("feed:")


post_service = PostService()
