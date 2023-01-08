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
            get_session_mock.assert_called_with()

        @patch("models.services.user.get_session")
        def test_create_user_raise_user_already_exist_error(
            self, get_session_mock: Mock,  db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            UserDBService.create_user("test_login", "test_password")

            with pytest.raises(UserAlreadyExistError, match=""):
                UserDBService.create_user("test_login", "test_password")

            get_session_mock.assert_called_with()

    class TestGetUser:
        @patch("models.services.user.get_session")
        def test_get_user_by_id_success(
            self, get_session_mock: Mock, db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = User(login="test_login", password="test_password")
            db_session.add(user)
            db_session.commit()

            user_ = UserDBService.get_user(user_id=1)

            assert user == user_
            get_session_mock.assert_called_with()

        @patch("models.services.user.get_session")
        def test_get_user_by_id_not_found(
            self, get_session_mock: Mock, db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = User(login="test_login", password="test_password")
            db_session.add(user)
            db_session.commit()

            user_ = UserDBService.get_user(user_id=2)

            assert user_ is None
            get_session_mock.assert_called_with()

        @patch("models.services.user.get_session")
        def test_get_user_by_login_success(
            self, get_session_mock: Mock, db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = User(login="test_login", password="test_password")
            db_session.add(user)
            db_session.commit()

            user_ = UserDBService.get_user(login="test_login")

            assert user == user_
            get_session_mock.assert_called_with()

        @patch("models.services.user.get_session")
        def test_get_user_by_login_not_found(
            self, get_session_mock: Mock, db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = User(login="test_login", password="test_password")
            db_session.add(user)
            db_session.commit()

            user_ = UserDBService.get_user(login="not_existed")

            assert user_ is None
            get_session_mock.assert_called_with()

    class TestUpdateUser:
        @patch("models.services.user.get_session")
        def test_update_user_password(
            self, get_session_mock: Mock, db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = User(login="test_login", password="test_password")
            db_session.add(user)
            db_session.commit()

            user_ = UserDBService.update_user(user, password="new_password")

            assert user_.password == "new_password"
            get_session_mock.assert_called_with()

        @patch("models.services.user.get_session")
        def test_update_user_name(
            self, get_session_mock: Mock, db_session: Session, clear_db
        ):
            get_session_mock.return_value = db_session
            user = User(login="test_login", password="test_password")
            db_session.add(user)
            db_session.commit()

            user_ = UserDBService.update_user(user, name="new_name")

            assert user_.name == "new_name"
            get_session_mock.assert_called_with()
