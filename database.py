import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from cfg import DB_STRING  # подгружаем из конфиг файлика тип и путь к БД

Base = declarative_base()


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


class Handler:
    session: sqlalchemy.orm.session.Session

    def __init__(self, base=Base):
        engine = sqlalchemy.create_engine('postgresql+psycopg2://api:tushpy@localhost/api_db')
        base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        self.session_maker = scoped_session(session_factory)

    def dbconnect(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = self.session_maker()  
            try:
                func(session, *args, **kwargs)
                session.commit()
            except Exception as ex:
                logging.error(ex)
                session.rollback()
                raise
            finally:
                self.session_maker.remove()  

        return wrapper


h = Handler()


@h.dbconnect
def create_users(session):
    session.add(User("jopa"))


@h.dbconnect
def list_users(session):
    print(session.query(User).all())


if __name__ == '__main__':
    list_users()
