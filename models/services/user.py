from typing import Optional

from pydantic.types import PositiveInt
from sqlalchemy.exc import IntegrityError

from clients.database import get_session
from models.user import User
from utils.errors import UserAlreadyExistError


class UserDBService:
    @staticmethod
    def create_user(login: str, password: str) -> User:
        with get_session() as session:
            user = User(login=login, password=password)
            session.add(user)
            try:
                session.commit()
                session.refresh(user)
            except IntegrityError:
                session.rollback()
                session.close()
                raise UserAlreadyExistError
        return user

    @staticmethod
    def get_user(user_id: Optional[PositiveInt] = None, login: Optional[str] = None) -> Optional[User]:
        filters = []
        if user_id:
            filters.append(User.id == user_id)
        if login:
            filters.append(User.login == login)
        with get_session() as session:
            result = session.query(User).filter(*filters).first()
        return result

    @staticmethod
    def update_user(user_model: User, password: Optional[str] = None, name: Optional[str] = None) -> User:
        if password:
            user_model.password = password
        if name:
            user_model.name = name
        with get_session() as session:
            session.add(user_model)
        return user_model
