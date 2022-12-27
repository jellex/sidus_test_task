from datetime import timedelta
from typing import Dict, Optional, Tuple, Union

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth import AuthJWT
from pydantic.types import PositiveInt

token_expire_time = timedelta(hours=24)


def create_access_refresh_tokens(
    authorize: AuthJWT,
    login: str,
    user_id: Optional[PositiveInt] = None,
) -> Tuple[str, str]:
    user_claims = {}
    if user_id:
        user_claims.update(user_id=user_id)

    access_token = authorize.create_access_token(
        subject=login, user_claims=user_claims, expires_time=token_expire_time
    )
    refresh_token = authorize.create_refresh_token(
        subject=login,
        user_claims=user_claims,
    )
    return access_token, refresh_token


def create_access_token(
    authorize: AuthJWT,
    login: str,
    user_id: Optional[PositiveInt] = None,
) -> str:
    user_claims = {}
    if user_id:
        user_claims.update(user_id=user_id)

    return authorize.create_access_token(
        subject=login,
        user_claims=user_claims,
        expires_time=token_expire_time,
    )


def get_user_id_from_jwt(authorize: AuthJWT) -> Optional[PositiveInt]:
    raw_jwt: Optional[Dict[str, Union[str, int, bool]]] = authorize.get_raw_jwt()
    if not raw_jwt:
        return
    user_id = raw_jwt.get("user_id")
    if user_id:
        user_id = int(user_id)
    return user_id


def check_jwt_auth_and_return_user_id(authorize: AuthJWT = Depends()) -> PositiveInt:
    """Check JWT auth and return user_id if it successfully extracts from JWT"""
    authorize.jwt_required()

    user_id: Optional[PositiveInt] = get_user_id_from_jwt(authorize)
    if not user_id:
        raise HTTPException(403, detail="Not authenticated")

    return user_id
