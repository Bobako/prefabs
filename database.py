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
        engine = sqlalchemy.create_engine(DB_STRING + '?check_same_thread=False')
        base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine, expire_on_commit=False)()
        print("База данных подключена.")


"Далее, например в мейн файле:" \
"(как вариант (если в нескольких файлах нужен доступ к бд) безусловно объявляем объект хендлера тут" \
"и используем конкретно его в других местах)"

from database import Handler
db = Handler()

some_object = db.session.query(SomeClass).filter(SomeClass.id == 1).one() # ну и флексим с сессией как хотим
db.session.delete(some_object)
db.session.commit()
