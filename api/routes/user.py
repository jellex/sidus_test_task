from fastapi import APIRouter
from fastapi.params import Body, Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT
from pydantic.types import PositiveInt

from models.user import User, AuthUser, UpdateUser, CreateUser
from services.user import UserService
from utils.jwt import check_jwt_auth_and_return_user_id, create_access_token

user_router = APIRouter()


@user_router.get("/get_user/", response_model=User)
async def get_user(
    user_id: PositiveInt = Body(...),
) -> User:
    user = await UserService.get_user(user_id)
    return user


@user_router.post("/create_user/", response_model=CreateUser)
async def create_user(
    user: AuthUser = Body(...),
    authorize: AuthJWT = Depends(),
) -> CreateUser:
    user_ = await UserService.create_user(user.login, user.password)
    access_token = create_access_token(authorize, user_.login, user_.id)

    return CreateUser(**user_.dict(), access_token=access_token)


@user_router.patch("/update_user/", dependencies=[Depends(HTTPBearer())], response_model=User)
async def update_user(
    user_id: PositiveInt = Depends(check_jwt_auth_and_return_user_id),
    user: UpdateUser = Body(...),
) -> User:
    user_ = await UserService.update_user(user_id, user.password, user.name)
    return user_
