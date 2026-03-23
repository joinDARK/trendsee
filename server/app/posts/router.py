import asyncio
import json
import uuid

from authx.schema import TokenPayload
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import exists, select
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from app.config import SETTINGS
from app.dependencies import RedisDependency, SessionDependency
from app.posts.models import Post
from app.posts.schemas import CachedPostSchema, PostSchema
from app.users.models import User
from app.utils import auth

posts_router = APIRouter(prefix="/u/{user_id}/p", tags=["Posts"])


@posts_router.get("/")
async def get_all_post(user_id: uuid.UUID, session: SessionDependency):
    stmt = select(exists().where(User.id == user_id))
    exists_flag = await session.scalar(stmt)
    if exists_flag is False:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    await asyncio.sleep(2)  # симуляция нагрузки

    result = await session.execute(select(Post).where(Post.user_id == user_id))
    posts = result.scalars().all()
    return list(posts)


@posts_router.get("/{post_id}")
async def get_user_post(
    user_id: uuid.UUID, post_id: int, session: SessionDependency, redis: RedisDependency
):
    stmt = select(exists().where(User.id == user_id))
    exists_flag = await session.scalar(stmt)
    if not exists_flag:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    # Пробуем получить из кэша
    post_key = f"u:{user_id}:p:{post_id}"
    cached_post = await redis.get(post_key)
    if cached_post:
        return CachedPostSchema.model_validate_json(cached_post)

    # Если кэша нет — идём в БД
    post = await session.scalar(
        select(Post).where(Post.id == post_id, Post.user_id == user_id)
    )
    if post is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")

    return post


@posts_router.post("/")
async def create(
    user_id: uuid.UUID,
    post: PostSchema,
    session: SessionDependency,
    redis: RedisDependency,
    payload: TokenPayload = Depends(auth.access_token_required),
):
    if payload.sub != str(user_id):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized request"
        )

    stmt = select(exists().where(User.id == payload.sub))
    exists_flag = await session.scalar(stmt)
    if exists_flag is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    new_post = Post(title=post.title, text=post.text, user_id=payload.sub)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)

    # Кэшируем пост
    post_key = f"u:{user_id}:p:{new_post.id}"
    await redis.setex(
        post_key,
        SETTINGS.POST_CACHE_TTL,
        CachedPostSchema(
            user_id=new_post.user_id,
            title=new_post.title,
            text=new_post.text,
            created_at=new_post.created_at,
        ).model_dump_json(),
    )

    return new_post


@posts_router.put("/{post_id}")
async def update(
    user_id: uuid.UUID,
    post_id: int,
    post: PostSchema,
    redis: RedisDependency,
    session: SessionDependency,
):
    stmt = select(exists().where(User.id == user_id))
    exists_flag = await session.scalar(stmt)
    if not exists_flag:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    existing_post = await session.scalar(
        select(Post).where(Post.id == post_id, Post.user_id == user_id)
    )
    if existing_post is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")

    existing_post.title = post.title
    existing_post.text = post.text
    await session.commit()
    await session.refresh(existing_post)
    post_key = f"u:{user_id}:p:{post_id}"
    if await redis.exists(post_key):
        await redis.set(
            post_key,
            CachedPostSchema(
                user_id=existing_post.user_id,
                title=existing_post.title,
                text=existing_post.text,
                created_at=existing_post.created_at,
            ).model_dump_json(),
            keepttl=True,
        )

    return existing_post


@posts_router.delete("/{post_id}")
async def delete(
    user_id: uuid.UUID, post_id: int, session: SessionDependency, redis: RedisDependency
):
    stmt = select(exists().where(User.id == user_id))
    exists_flag = await session.scalar(stmt)
    if not exists_flag:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    existing_post = await session.scalar(
        select(Post).where(Post.id == post_id, Post.user_id == user_id)
    )
    if existing_post is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")

    await session.delete(existing_post)
    await session.commit()
    await redis.delete(f"u:{user_id}:p:{post_id}")
    return {"success": True}
