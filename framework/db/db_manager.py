from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import declarative_base
from ..metaclass.singleton_meta import SingletonMeta
from .db_properties import DatasourceProperties


class DbManager(metaclass=SingletonMeta):
    def __init__(self):
        self._db_properties = DatasourceProperties()
        db_url = "{dialect}+{driver}://{user}:{password}@{host}/{dbname}".format(
            dialect=self._db_properties.dialect,
            driver=self._db_properties.driver,
            user=self._db_properties.user,
            password=self._db_properties.password,
            host=self._db_properties.host,
            dbname=self._db_properties.dbname
        )
        self._engine = create_engine(db_url)
        self._session_factory = scoped_session(sessionmaker(bind=self._engine))

    def get_session(self) -> Session:
        return self._session_factory()

    def init_db(self):
        self.get_base().metadata.create_all()

    def get_base(self):
        return declarative_base(bind=self._engine)
