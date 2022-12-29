import pytest

from models.user import User


@pytest.fixture()
def user_db_fixture():
    # password = "test_password"
    # HasherService.get_password_hash("test_password") ->
    # $2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi
    return User(
        id=1,
        login="test_user",
        password="$2b$12$O3MYXaKY5uw6TJ9PSQDI5uCMh3bj8ZQjpAUtkhinrRDiOQhSkuUEi",
    )
