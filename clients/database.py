from contextlib import contextmanager

from sqlmodel import Session, create_engine

import models  # noqa
from config import config

connect_args = {"connect_timeout": 10}
engine = create_engine(
    config.DATABASE_URL, pool_size=3, max_overflow=0, connect_args=connect_args
)


@contextmanager
def get_session(engine_=None) -> Session:
    if not engine_:
        engine_ = engine
    session = Session(engine_)
    try:
        yield session
    finally:
        session.close()
