import functools
from contextlib import contextmanager
from sqlalchemy.orm import Session
from .db_manager import DbManager


def db_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return func(*args, **kwargs)
        with get_session() as session:
            return func(*args, session=session, **kwargs)
    return wrapper


@contextmanager
def transaction(session: Session):
    if not session.transaction:
        with session.begin():
            yield
    else:
        yield


@contextmanager
def get_session() -> Session:
    try:
        session = DbManager().get_session()
        yield session
    finally:
        if session:
            session.close()
