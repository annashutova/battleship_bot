from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_HOST: str = 'http://172.0.0.4:8000'

    BOT_TOKEN: str = ''
    WEBHOOK_URL: str = ''

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str =''
    REDIS_DB: int = 0

    LOG_LEVEL: str = 'debug'

    RETRY_COUNT: int = 3


settings = Settings()