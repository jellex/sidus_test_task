from pydantic import AnyHttpUrl, BaseSettings

from config.auth import AuthConfig
from config.database import DatabaseConfig
from config.redis import RedisConfig


class Config(BaseSettings, AuthConfig, DatabaseConfig, RedisConfig):
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"
    WORKERS: int = 1
    IS_DEBUG: bool = True


config = Config()
