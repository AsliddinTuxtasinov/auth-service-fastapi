import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = 'auth-service'
    APP_VERSION: str = '0.0.1'
    APP_DESCRIPTION: str = 'Auth Service'
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
