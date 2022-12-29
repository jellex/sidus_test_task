from unittest.mock import patch, AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from models.user import User
from utils.errors import UserDoesNotExistError

get_user_url = "/get_user"
create_user_url = "/create_user"
update_user_url = "/update_user"
user_service_path = "api.routes.user.UserService"


class TestGetUser:
    @pytest.mark.asyncio()
    @patch(f"{user_service_path}.get_user")
    async def test_get_user_successfully(self, get_user_mock: AsyncMock, client: TestClient, user_db_fixture: User):
        get_user_mock.return_value = user_db_fixture

        result = client.get(f"{get_user_url}/1")
        assert result.status_code == 200
        assert result.json() == {
            "id": 1,
            "login": "test_user",
            "name": None,
            "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
        }

        get_user_mock.assert_awaited_with(1)

    @pytest.mark.asyncio()
    @patch(f"{user_service_path}.get_user")
    async def test_get_user_does_not_exist_error(self, get_user_mock: AsyncMock, client: TestClient, user_db_fixture: User):
        get_user_mock.side_effect = UserDoesNotExistError

        result = client.get(f"{get_user_url}/1")
        assert result.status_code == 404
        assert result.json() == {
            "detail": "user doesn't exist"
        }

        get_user_mock.assert_awaited_with(1)

    @pytest.mark.asyncio()
    async def test_get_user_wrong_input_param_type(self, client: TestClient, user_db_fixture: User):
        result = client.get(f"{get_user_url}/x")
        assert result.status_code == 422
        assert result.json() == {
            "detail": [
                {
                    "loc": ["path", "user_id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer"
                }
            ]
        }

    @pytest.mark.asyncio()
    async def test_get_user_skip_required_param(self, client: TestClient, user_db_fixture: User):
        result = client.get(f"{get_user_url}/")
        assert result.status_code == 404
        assert result.json() == {
            "detail": "Not Found"
        }


class TestCreateUser:
    @pytest.mark.asyncio()
    @patch("api.routes.user.create_access_token")
    @patch(f"{user_service_path}.create_user")
    async def test_create_user_successfully(
        self, create_user_mock: AsyncMock,
        create_access_token_mock: Mock,
        client: TestClient,
        user_db_fixture: User
    ):
        create_user_mock.return_value = user_db_fixture
        create_access_token_mock.return_value = "test_access_token"

        result = client.post(f"{create_user_url}/", json={"login": "test_user", "password": "test_password"})
        assert result.status_code == 200
        assert result.json() == {
            "id": 1,
            "login": "test_user",
            "name": None,
            "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
            "access_token": "test_access_token",
        }

        create_user_mock.assert_awaited_with("test_user", "test_password")

    @pytest.mark.asyncio()
    async def test_create_user_skip_required_param(
        self,
        client: TestClient,
        user_db_fixture: User
    ):
        result = client.post(f"{create_user_url}/", json={"login": "test_user", "password_wrong": "test_password"})
        assert result.status_code == 422
        assert result.json() == {
            "detail": [
                {
                    "loc": ["body", "password"],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }


class TestUpdateUser:
    @pytest.mark.asyncio()
    @patch(f"{user_service_path}.update_user")
    async def test_update_user_successfully(
        self, update_user_mock: AsyncMock,
        client: TestClient,
        user_db_fixture: User,
        jwt_for_user_fixture: str
    ):
        user_db_fixture.name = "new_name"
        update_user_mock.return_value = user_db_fixture

        result = client.patch(f"{update_user_url}/", json={"user_id": 1, "name": "new_name"}, headers={"Authorization": f"Bearer {jwt_for_user_fixture}"})
        assert result.status_code == 200
        assert result.json() == {
            "id": 1,
            "login": "test_user",
            "name": "new_name",
            "password": "$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
        }

        update_user_mock.assert_awaited_with(1, None, "new_name")

    @pytest.mark.asyncio()
    @patch(f"{user_service_path}.update_user")
    async def test_update_user_does_not_exist_error(
        self, update_user_mock: AsyncMock,
        client: TestClient,
        user_db_fixture: User,
        jwt_for_user_fixture: str
    ):
        update_user_mock.side_effect = UserDoesNotExistError

        result = client.patch(
            f"{update_user_url}/",
            json={"user_id": 1, "name": "new_name"},
            headers={"Authorization": f"Bearer {jwt_for_user_fixture}"}
        )
        assert result.status_code == 404
        assert result.json() == {
            "detail": "user doesn't exist"
        }

        update_user_mock.assert_awaited_with(1, None, "new_name")

    @pytest.mark.asyncio()
    async def test_update_user_skip_required_param(
        self,
        client: TestClient,
        user_db_fixture: User,
        jwt_for_user_fixture: str
    ):
        result = client.patch(
            f"{update_user_url}/",
            headers={"Authorization": f"Bearer {jwt_for_user_fixture}"}
        )
        assert result.status_code == 422
        assert result.json() == {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }

    @pytest.mark.asyncio()
    async def test_update_user_unauthorized_access(
        self,
        client: TestClient,
        user_db_fixture: User,
        jwt_for_user_fixture: str
    ):
        result = client.patch(
            f"{update_user_url}/",
            json={"user_id": "x", "name": "new_name"},
        )
        assert result.status_code == 403
        assert result.json() == {
            "detail": "Not authenticated"
        }
