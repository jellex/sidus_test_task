import pydantic
from fastapi import FastAPI, Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse
from sqlmodel import SQLModel

from api.routes import (
    user_router,
)
from clients.database import engine
from config import Config
from utils.errors import UserDoesNotExistError


def init_api(config: Config):
    app = FastAPI(
        title="Sidus API",
        description="",
        version="0",
        docs_url="/",
        redoc_url="/docs",
        openapi_tags=[],
    )
    # pass config object to application
    app.config = config

    _cors(app)
    _gzip(app)
    _routes(app)

    _register_exception_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        # create database and table
        SQLModel.metadata.create_all(engine)

    @app.on_event("shutdown")
    async def shutdown_event():
        pass

    return app


def _cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _gzip(app: FastAPI):
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )


def _routes(app: FastAPI):
    app.include_router(user_router, tags=["User"])


def _register_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def common_exception_handler(
        request: Request,
        exc: Exception,
    ):
        exception_dict = {
            "type": "Internal Server Error",
            "title": exc.__class__.__name__,
            "instance": request.url.path,
            "detail": f"{exc.__class__.__name__} at {str(exc)} when executing {request.method} request",
        }
        return JSONResponse(exception_dict, status_code=500)

    @app.exception_handler(ValueError)
    async def value_error_exception_handler(
        request: Request,
        exc: ValueError,
    ):
        exception_dict = {
            "type": "Value Error",
            "title": exc.__class__.__name__,
            "instance": request.url.path,
            "detail": f"{exc.__class__.__name__} at {str(exc)} when executing {request.method} request",
        }
        return JSONResponse(exception_dict, status_code=500)

    @app.exception_handler(pydantic.error_wrappers.ValidationError)
    async def handle_validation_error(
        request: Request,
        exc: pydantic.error_wrappers.ValidationError,
    ):
        exception_dict = {
            "type": "ValidationError",
            "title": exc.__class__.__name__,
            "instance": request.url.path,
            "detail": f"{exc.__class__.__name__} at {str(exc)} when executing {request.method} request",
        }
        return JSONResponse(exception_dict, status_code=422)

    # exception handler for jwt
    @app.exception_handler(AuthJWTException)
    def jwt_exception_handler(
        request: Request,
        exc: AuthJWTException,
    ):
        exception_dict = {
            "type": "AuthJWTException",
            "title": exc.__class__.__name__,
            "instance": request.url.path,
            "detail": exc.message,
        }
        return JSONResponse(exception_dict, status_code=exc.status_code)

    @app.exception_handler(UserDoesNotExistError)
    async def user_does_not_exist_exception_handler(
        request: Request, exc: UserDoesNotExistError
    ):
        if not exc.args:
            detail = "user doesn't exist"
        else:
            detail = str(exc)
        return JSONResponse({"detail": detail}, status_code=404)
