from typing import Annotated

from fastapi import Depends
from redis.client import Redis
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.redis import get_redis_client

SessionDependency = Annotated[AsyncSession, Depends(get_session)]
RedisDependency = Annotated[Redis, Depends(get_redis_client)]
