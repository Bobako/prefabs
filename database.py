import functools
import logging
from typing import Any

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session

Base = declarative_base()


class Database:
    session: sqlalchemy.orm.session.Session

    def __init__(self,
                 login: str,
                 password: str,
                 database_name: str,
                 host: str = "localhost",
                 database_type: str = "postgresql+psycopg2"):
        engine = sqlalchemy.create_engine(
            f'{database_type}://{login}:{password}@{host}/{database_name}')

        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        self.session_maker = scoped_session(session_factory)

    def get_session(self, func):
        """This is a decorator to give to a 
        function(session, *args, **kwargs) a proper scoped session"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = self.session_maker()
            res = None
            try:
                res = func(session, *args, **kwargs)
                session.commit()
            except Exception as ex:
                session.rollback()
                raise ex
            finally:
                self.session_maker.remove()
                return res

        return wrapper




"Примеры конкретных зависимостей:"
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    facility_id = Column(Integer, ForeignKey("facility.id"))  # зависимость один к многим; далее можно будет получить
    facility = relationship("Facility", bacref="users")       # user.facility - объект, на который ссылается user и
                                                              # facility.users - список объектов, которые ссылаются на данный
                                                              # Для добавления новой реляции устанваливаем соотв. id foreign_key'а,
                                                              # коммитим.

class Facility(Base):
    __tablename__ = "facility"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Type(Base):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    facilities = relationship('Facility', secondary='type_to_facility_association', lazy='dynamic', backref='types')

type_to_facility_association = Table(                                                   # отношение "многие к многим"
    'type_to_facility_association', Base.metadata,                                      # в обоих случаях получим списки
    Column('facility_id', Integer(), ForeignKey('facility.id'), primary_key=True),      # facility.types и type.facilities
    Column('type_id', Integer(), ForeignKey('type.id'), primary_key=True),              # ссылающихся объектов.
)                                                                                       # Для добавления новой реляции
                                                                                        # аппендим в список, коммитим бд





