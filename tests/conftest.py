from pathlib import Path

import pytest  # noqa
from aioredis import Redis
from fastapi.testclient import TestClient
from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel, create_engine

from api.init_api import FastAPI, init_api
from clients.database import get_session
from config import Config
from models.user import User
from tests.fixtures import *  # noqa

PROJECT_ROOT_PATH = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def config() -> Config:
    config = Config()
    config.DATABASE_URL = f"sqlite:///{PROJECT_ROOT_PATH}/test_db.sqlite"
    config.REDIS_URL = "redis://localhost/1"
    return config


@pytest.fixture()
def app(config: Config) -> FastAPI:
    app = init_api(config)
    yield app


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)


@pytest.fixture(scope="session")
def db_engine(config: Config) -> Engine:
    engine = create_engine(config.DATABASE_URL)
    # create database and table
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture()
def db_session(db_engine: Engine) -> Session:
    with get_session(db_engine) as session:
        yield session


@pytest.fixture()
def clear_db(db_session: Session) -> None:
    db_session.execute(User.__table__.delete())
    db_session.commit()
    yield
    db_session.execute(User.__table__.delete())
    db_session.commit()


@pytest.fixture()
def redis_client(config: Config) -> Redis:
    return Redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=True)
