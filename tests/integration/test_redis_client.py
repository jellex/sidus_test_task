import pytest
from aioredis import Redis


class TestRedisClient:
    @pytest.mark.asyncio()
    async def test_get_value_success(self, redis_client: Redis):
        await redis_client.delete(*["test"])
        await redis_client.set("test", 1)
        result = await redis_client.get("test")

        assert result == "1"

        await redis_client.delete(*["test"])

    @pytest.mark.asyncio()
    async def test_get_value_not_found(self, redis_client: Redis):
        result = await redis_client.get("test")

        assert result is None

    @pytest.mark.asyncio()
    async def test_set_value_success(self, redis_client: Redis):
        await redis_client.delete(*["test"])
        await redis_client.set("test", 1)
        result = await redis_client.get("test")

        assert result == "1"

        await redis_client.delete(*["test"])

    @pytest.mark.asyncio()
    async def test_delete_key_success(self, redis_client: Redis):
        await redis_client.set("test", 1)
        result = await redis_client.get("test")

        assert result == "1"

        await redis_client.delete(*["test"])
        result = await redis_client.get("test")

        assert result is None
