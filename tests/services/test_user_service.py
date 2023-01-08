from unittest.mock import AsyncMock, Mock, call, patch

import pytest

from models.user import User
from services.user import UserService
from utils.errors import UserAlreadyExistError, UserDoesNotExistError

user_db_service_path = "models.services.user.UserDBService"
hasher_service_path = "services.hashing.HasherService"
caching_service_path = "services.caching.CachingService"


class TestUserService:
    class TestCreateUser:
        @pytest.mark.asyncio()
        @patch(f"{user_db_service_path}.create_user")
        @patch(f"{hasher_service_path}.get_password_hash")
        async def test_create_user_successfully(
            self,
            get_password_hash_mock: Mock,
            create_user_mock: Mock,
            user_db_fixture: User,
        ):
            get_password_hash_mock.return_value = "hashed_password"
            user_db_fixture.password = "hashed_password"
            create_user_mock.return_value = user_db_fixture

            user = await UserService.create_user("test_login", "test_password")
            assert user == user_db_fixture

            get_password_hash_mock.assert_called_with("test_password")
            create_user_mock.assert_called_with("test_login", "hashed_password")

        @pytest.mark.asyncio()
        @patch(f"{user_db_service_path}.create_user")
        @patch(f"{hasher_service_path}.get_password_hash")
        async def test_create_user_already_existed(
            self,
            get_password_hash_mock: Mock,
            create_user_mock: Mock,
            user_db_fixture: User,
        ):
            get_password_hash_mock.return_value = "hashed_password"
            user_db_fixture.password = "hashed_password"
            create_user_mock.side_effect = UserAlreadyExistError

            with pytest.raises(UserAlreadyExistError, match=""):
                await UserService.create_user("test_login", "test_password")

            get_password_hash_mock.assert_called_with("test_password")
            create_user_mock.assert_called_with("test_login", "hashed_password")

    class TestGetUser:
        @pytest.mark.asyncio()
        @patch("logging.warning")
        @patch(f"{caching_service_path}.set_value")
        @patch(f"{user_db_service_path}.get_user")
        @patch(f"{caching_service_path}.get_value")
        async def test_get_user_by_user_id_from_cache(
            self,
            get_value_mock: AsyncMock,
            get_user_mock: Mock,
            set_value_mock: AsyncMock,
            warning_mock: Mock,
            user_db_fixture: User,
        ):
            get_value_mock.return_value = user_db_fixture.dict()

            user = await UserService.get_user(1)
            assert user == user_db_fixture

            get_value_mock.assert_called_with("Users:1-None")
            warning_mock.assert_called_with("cache hit")
            get_user_mock.assert_not_called()
            set_value_mock.assert_called_with(
                "Users:1-None",
                {
                    "name": None,
                    "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
                    "login": "test_user",
                    "id": 1,
                },
            )

        @pytest.mark.asyncio()
        @patch(f"{caching_service_path}.set_value")
        @patch(f"{user_db_service_path}.get_user")
        @patch(f"{caching_service_path}.get_value")
        async def test_get_user_by_user_id_from_database(
            self,
            get_value_mock: AsyncMock,
            get_user_mock: Mock,
            set_value_mock: AsyncMock,
            user_db_fixture: User,
        ):
            get_value_mock.return_value = None
            get_user_mock.return_value = user_db_fixture

            user = await UserService.get_user(1)
            assert user == user_db_fixture

            get_value_mock.assert_called_with("Users:1-None")
            get_user_mock.assert_called_with(1, None)
            set_value_mock.assert_called_with(
                "Users:1-None",
                {
                    "name": None,
                    "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
                    "login": "test_user",
                    "id": 1,
                },
            )

        @pytest.mark.asyncio()
        @patch(f"{caching_service_path}.set_value")
        @patch(f"{user_db_service_path}.get_user")
        @patch(f"{caching_service_path}.get_value")
        async def test_get_user_by_user_id_user_does_not_exist(
            self,
            get_value_mock: AsyncMock,
            get_user_mock: Mock,
            set_value_mock: AsyncMock,
            user_db_fixture: User,
        ):
            get_value_mock.return_value = None
            get_user_mock.return_value = None

            with pytest.raises(UserDoesNotExistError):
                await UserService.get_user(1)

            get_value_mock.assert_called_with("Users:1-None")
            get_user_mock.assert_called_with(1, None)
            set_value_mock.assert_not_called()

        @pytest.mark.asyncio()
        @patch("logging.warning")
        @patch(f"{caching_service_path}.set_value")
        @patch(f"{user_db_service_path}.get_user")
        @patch(f"{caching_service_path}.get_value")
        async def test_get_user_by_login_from_cache(
            self,
            get_value_mock: AsyncMock,
            get_user_mock: Mock,
            set_value_mock: AsyncMock,
            warning_mock: Mock,
            user_db_fixture: User,
        ):
            get_value_mock.return_value = user_db_fixture.dict()

            user = await UserService.get_user(login="test_user")
            assert user == user_db_fixture

            get_value_mock.assert_called_with("Users:None-test_user")
            warning_mock.assert_called_with("cache hit")
            get_user_mock.assert_not_called()
            set_value_mock.assert_called_with(
                "Users:None-test_user",
                {
                    "name": None,
                    "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
                    "login": "test_user",
                    "id": 1,
                },
            )

        @pytest.mark.asyncio()
        @patch(f"{caching_service_path}.set_value")
        @patch(f"{user_db_service_path}.get_user")
        @patch(f"{caching_service_path}.get_value")
        async def test_get_user_by_login_from_database(
            self,
            get_value_mock: AsyncMock,
            get_user_mock: Mock,
            set_value_mock: AsyncMock,
            user_db_fixture: User,
        ):
            get_value_mock.return_value = None
            get_user_mock.return_value = user_db_fixture

            user = await UserService.get_user(login="test_user")
            assert user == user_db_fixture

            get_value_mock.assert_called_with("Users:None-test_user")
            get_user_mock.assert_called_with(None, "test_user")
            set_value_mock.assert_called_with(
                "Users:None-test_user",
                {
                    "name": None,
                    "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
                    "login": "test_user",
                    "id": 1,
                },
            )

        @pytest.mark.asyncio()
        @patch(f"{caching_service_path}.set_value")
        @patch(f"{user_db_service_path}.get_user")
        @patch(f"{caching_service_path}.get_value")
        async def test_get_user_by_login_user_does_not_exist(
            self,
            get_value_mock: AsyncMock,
            get_user_mock: Mock,
            set_value_mock: AsyncMock,
            user_db_fixture: User,
        ):
            get_value_mock.return_value = None
            get_user_mock.return_value = None

            with pytest.raises(UserDoesNotExistError):
                await UserService.get_user(login="test_user")

            get_value_mock.assert_called_with("Users:None-test_user")
            get_user_mock.assert_called_with(None, "test_user")
            set_value_mock.assert_not_called()

    class TestUpdateUser:
        @pytest.mark.asyncio()
        @patch(f"{caching_service_path}.delete_key")
        @patch(f"{user_db_service_path}.update_user")
        @patch(f"{user_db_service_path}.get_user")
        async def test_update_user_successfully(
            self,
            get_user_mock: Mock,
            update_user_mock: Mock,
            delete_key_mock: AsyncMock,
            user_db_fixture: User,
        ):
            get_user_mock.return_value = user_db_fixture
            user_db_fixture.name = "new_name"
            update_user_mock.return_value = user_db_fixture

            user = await UserService.update_user(1, name="new_name")
            assert user == user_db_fixture

            get_user_mock.assert_called_with(1)
            update_user_mock.assert_called_with(user_db_fixture, None, "new_name")
            delete_key_mock.assert_has_calls(
                [
                    call(f"Users:1-test_user"),
                    call(f"Users:1-None"),
                    call(f"Users:None-test_user"),
                ]
            )

        @pytest.mark.asyncio()
        @patch(f"{caching_service_path}.delete_key")
        @patch(f"{user_db_service_path}.update_user")
        @patch(f"{user_db_service_path}.get_user")
        async def test_update_user_user_does_not_exist_error(
            self,
            get_user_mock: Mock,
            update_user_mock: Mock,
            delete_key_mock: AsyncMock,
            user_db_fixture: User,
        ):
            get_user_mock.return_value = None

            with pytest.raises(UserDoesNotExistError):
                await UserService.update_user(1, name="new_name")

            get_user_mock.assert_called_with(1)
            update_user_mock.assert_not_called()
            delete_key_mock.assert_not_called()
