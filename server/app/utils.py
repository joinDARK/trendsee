from authx import AuthX, AuthXConfig

from app.config import SETTINGS

config = AuthXConfig(
    JWT_SECRET_KEY=SETTINGS.JWT_ACCESS_SECRET, JWT_TOKEN_LOCATION=["headers"]
)

auth = AuthX(config=config)
