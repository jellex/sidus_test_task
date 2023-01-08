import asyncio
import logging
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
    async def get_user(
        user_id: Optional[PositiveInt] = None, login: Optional[str] = None
    ) -> User:
        user = await CachingService.get_value(f"Users:{user_id}-{login}")
        if user:
            user = User(**user)
            logging.warning("cache hit")
        else:
            user = UserDBService.get_user(user_id, login)
            logging.warning("cache miss")
        if not user:
            raise UserDoesNotExistError
        await CachingService.set_value(f"Users:{user_id}-{login}", user.dict())
        return user

    @staticmethod
    async def update_user(
        user_id: PositiveInt, password: Optional[str] = None, name: Optional[str] = None
    ) -> User:
        user = UserDBService.get_user(user_id)
        if not user:
            raise UserDoesNotExistError
        updated_user = UserDBService.update_user(user, password, name)
        await asyncio.gather(
            CachingService.delete_key(f"Users:{updated_user.id}-{updated_user.login}"),
            CachingService.delete_key(f"Users:{updated_user.id}-None"),
            CachingService.delete_key(f"Users:None-{updated_user.login}"),
        )
        return updated_user
