from pydantic import AnyUrl, BaseModel


class RedisConfig(BaseModel):
    REDIS_URL: AnyUrl = "redis://localhost"
