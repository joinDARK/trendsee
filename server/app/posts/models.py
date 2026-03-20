import uuid

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BigInteger

from app.database import Base, created_at, updated_at


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(
        Text,
        index=True,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    created_at: Mapped[updated_at]
    updated_at: Mapped[created_at]
