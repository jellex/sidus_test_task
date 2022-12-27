from typing import Optional

from pydantic.types import PositiveInt

from models.services.user import UserDBService
from models.user import User
from services.hashing import HasherService
from utils.errors import UserDoesNotExistError


class UserService:
    @staticmethod
    async def create_user(login: str, password: str) -> User:
        hashed_password = HasherService.get_password_hash(password)
        user = UserDBService.get_user(login=login)
        if not user:
            user = UserDBService.create_user(login, hashed_password)
        return user

    @staticmethod
    async def get_user(user_id: Optional[PositiveInt] = None, login: Optional[str] = None) -> User:
        user = UserDBService.get_user(user_id, login)
        if not user:
            raise UserDoesNotExistError
        return user

    @staticmethod
    async def update_user(user_id: PositiveInt, password: Optional[str] = None, name: Optional[str] = None) -> User:
        user = UserDBService.get_user(user_id)
        if not user:
            raise UserDoesNotExistError
        updated_user = UserDBService.update_user(user, password, name)
        return updated_user
