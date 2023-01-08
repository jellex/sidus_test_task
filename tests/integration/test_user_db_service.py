from unittest.mock import patch, Mock

import pytest
from sqlmodel import Session

from models.services.user import UserDBService
from models.user import User
from utils.errors import UserAlreadyExistError


class TestUserDBService:
    class TestCreateUser:
        @patch("models.services.user.get_session")
        def test_create_user_success(
            self, get_session_mock: Mock,  db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = UserDBService.create_user("test_login", "test_password")

            assert isinstance(user, User)
            assert user.id == 1
            assert user.login == "test_login"
            assert user.password == "test_password"

            user_ = db_session.query(User).get(1)

            assert user_ == user

        @patch("models.services.user.get_session")
        def test_create_user_raise_user_already_exist_error(
            self, get_session_mock: Mock,  db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            UserDBService.create_user("test_login", "test_password")

            with pytest.raises(UserAlreadyExistError, match=""):
                UserDBService.create_user("test_login", "test_password")
