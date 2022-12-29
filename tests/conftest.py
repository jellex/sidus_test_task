from pathlib import Path

import pytest  # noqa
from fastapi.testclient import TestClient

from api.init_api import FastAPI, init_api
from clients.database import get_session
from config import Config
from models.user import User
from tests.fixtures import *  # noqa

PROJECT_ROOT_PATH = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def config() -> Config:
    config = Config()
    config.DATABASE_URL = f"sqlite:{PROJECT_ROOT_PATH}/test_db.sqlite"
    return config


@pytest.fixture()
def app(config: Config) -> FastAPI:
    app = init_api(config)
    yield app


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)


@pytest.fixture()
def clear_db() -> None:
    with get_session() as db_session:
        db_session.execute(User.__table__.delete())
        db_session.commit()
    yield
    with get_session() as db_session:
        db_session.execute(User.__table__.delete())
        db_session.commit()
