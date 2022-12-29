import pytest
from fastapi_jwt_auth import AuthJWT

from models.user import User
from utils.jwt import create_access_token


@pytest.fixture()
def jwt_for_user_fixture(user_db_fixture: User) -> str:
    authorize = AuthJWT()
    access_token = create_access_token(
        authorize, user_db_fixture.login, user_db_fixture.id
    )
    return access_token
