from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int


@lru_cache
def get_settings():
    return Settings()
