__all__ = ("Base", "User", "Post")

from app.database import Base
from app.posts.models import Post
from app.users.models import User

