from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_HOST: str = 'http://172.0.0.2:8000'
    BOT_TOKEN: str


settings = Settings()
