from typing import Optional

from pydantic.types import PositiveInt

from models.services.user import UserDBService
from models.user import User
from services.caching import CachingService
from services.hashing import HasherService
from utils.errors import UserDoesNotExistError


class UserService:
    @staticmethod
    async def create_user(login: str, password: str) -> User:
        hashed_password = HasherService.get_password_hash(password)
        user = UserDBService.create_user(login, hashed_password)
        return user

    @staticmethod
    async def get_user(user_id: Optional[PositiveInt] = None, login: Optional[str] = None) -> User:
        user = await CachingService.get_value(f"Users:{user_id}")
        if user:
            user = User(**user)
            print("cache hit")
        else:
            user = UserDBService.get_user(user_id, login)
            print("cache miss")
        if not user:
            raise UserDoesNotExistError
        await CachingService.set_value(f"Users:{user.id}", user.dict())
        return user

    @staticmethod
    async def update_user(user_id: PositiveInt, password: Optional[str] = None, name: Optional[str] = None) -> User:
        user = UserDBService.get_user(user_id)
        if not user:
            raise UserDoesNotExistError
        updated_user = UserDBService.update_user(user, password, name)
        await CachingService.delete_key(f"Users:{updated_user.id}")
        return updated_user
