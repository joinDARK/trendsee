from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWT_ACCESS_SECRET: str
    POST_CACHE_TTL: int = 600

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# TODO: пределать так, чтобы данные поставлялись из env
SETTINGS = Settings(
    DB_HOST="localhost",
    DB_PORT=5432,
    DB_USER="postgres",
    DB_PASS="1234",
    DB_NAME="trendsee",
    JWT_ACCESS_SECRET="sec",
)
