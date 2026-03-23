from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "1234"
    DB_NAME: str = "trendsee"
    JWT_ACCESS_SECRET: str = "sec"
    POST_CACHE_TTL: int = 600
    REDIS_HOST: str = "localhost"

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


SETTINGS = Settings()
