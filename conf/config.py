from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_HOST: str

    BOT_TOKEN: str
    WEBHOOK_URL: str = ''

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int

    METRICS_PORT: int

    LOG_LEVEL: str

    RETRY_COUNT: int = 3


settings = Settings()
