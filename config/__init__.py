from pydantic import AnyHttpUrl

from config.auth import AuthConfig
from config.database import DatabaseConfig


class Config(AuthConfig, DatabaseConfig):
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"
    WORKERS: int = 1
    IS_DEBUG: bool = True


config = Config()
