import json
from typing import Optional, Union

from clients.redis import redis_client


class CachingService:
    @staticmethod
    async def get_value(
        key: str,
    ) -> Optional[Union[str, dict, list, bytes, int, float]]:
        value = await redis_client.get(key)
        if value:
            return json.loads(value)

    @staticmethod
    async def set_value(
        key: str, value: Union[str, dict, list, bytes, int, float]
    ) -> None:
        new_value = json.dumps(value)
        return await redis_client.set(key, new_value)

    @staticmethod
    async def delete_key(key: str) -> None:
        return await redis_client.delete(*[key])
