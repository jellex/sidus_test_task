from unittest.mock import AsyncMock, patch

import pytest

from services.caching import CachingService


class TestCachingService:
    class TestGetValue:
        @pytest.mark.asyncio()
        @patch("services.caching.redis_client.get", new_callable=AsyncMock)
        async def test_get_value_success(self, get_value_mock: AsyncMock):
            get_value_mock.return_value = "1"

            result = await CachingService.get_value("test")

            assert result == 1
            get_value_mock.assert_awaited_with("test")

        @pytest.mark.asyncio()
        @patch("services.caching.redis_client.get", new_callable=AsyncMock)
        async def test_get_value_not_found(self, get_value_mock: AsyncMock):
            get_value_mock.return_value = None

            result = await CachingService.get_value("test")

            assert result is None

    class TestSetValue:
        @pytest.mark.asyncio()
        @patch("services.caching.redis_client.set", new_callable=AsyncMock)
        async def test_set_value_success(self, set_value_mock: AsyncMock):
            set_value_mock.return_value = "1"

            await CachingService.set_value("test", 1)

            set_value_mock.assert_awaited_with("test", "1")

    class TestDeleteKey:
        @pytest.mark.asyncio()
        @patch("services.caching.redis_client.delete", new_callable=AsyncMock)
        async def test_delete_key_success(self, delete_key_mock: AsyncMock):
            await CachingService.delete_key("test")

            delete_key_mock.assert_awaited_with(*["test"])
