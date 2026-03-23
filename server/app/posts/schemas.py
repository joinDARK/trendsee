import uuid
from datetime import datetime

from pydantic.fields import Field
from pydantic.main import BaseModel


class PostSchema(BaseModel):
    title: str = Field(max_length=255)
    text: str


class CachedPostSchema(PostSchema):
    user_id: uuid.UUID
    created_at: datetime
