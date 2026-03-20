from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.types import DateTime

from app.config import SETTINGS

engine = create_async_engine(url=SETTINGS.database_url_asyncpg, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=datetime.now,  # автообновление при UPDATE
        nullable=False,
    ),
]

created_at = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    ),
]
