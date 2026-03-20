from pydantic.fields import Field
from pydantic.main import BaseModel


class UserSchema(BaseModel):
    name: str = Field(max_length=255)
