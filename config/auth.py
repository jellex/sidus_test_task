from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class AuthConfig(BaseModel):
    authjwt_secret_key: str = (
        "ec5d56eaef1ef227718c8711c142cb46dba477f1812b8b556a3629d2aa720425"
    )


@AuthJWT.load_config
def get_config():
    return AuthConfig()
