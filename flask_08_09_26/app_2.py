# Урок 08.09.26 (часть 2): три способа связать класс Python с таблицей БД.
# Варианты 1-3 закомментированы и оставлены для сравнения, рабочий код — в конце файла.

# Table/Column/MetaData — «ядровой» (Core) способ описания схемы, без ORM-классов.
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# registry — низкоуровневый реестр сопоставлений (нужен для императивного маппинга).
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry, Mapped, mapped_column

# automap_base — автоматически строит классы по УЖЕ существующим таблицам в БД.
from sqlalchemy.ext.automap import automap_base

# VAR 1
# Императивный (classical) маппинг: схема таблицы и обычный Python-класс
# описываются ОТДЕЛЬНО, а затем связываются вызовом map_imperatively.
# Полезно, когда класс нельзя менять (чужая библиотека, готовая доменная модель).

# mapped_register = registry()
#
# user_table = Table('users', mapped_register.metadata,
#                    Column('id', Integer, primary_key=True),
#                    Column('username', String(30)),
#                    Column('age', Integer),
#                    )
#
# class User:
#     def __init__(self, username, age):
#         self.username = username
#         self.age = age
#
#
# mapped_register.map_imperatively(User, user_table)

# VAR 2
# Декларативный маппинг — основной и рекомендуемый способ в SQLAlchemy 2.0:
# класс и схема описываются вместе. Именно он используется в рабочем коде ниже.

# class Base(DeclarativeBase):
#     pass
#
# class User(Base):
#     __tablename__ = 'users'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(String(30))
#     age: Mapped[int] = mapped_column(Integer)
#
#
# engine = create_engine('sqlite:///db.sqlite')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
#
#
# with Session() as session:
#     pass

# VAR 3
# Автомаппинг (reflection): схему НЕ описываем вообще — SQLAlchemy читает её
# из уже существующей базы и сам генерирует классы.
# Удобно для работы с чужой/легаси-базой, но нет подсказок типов в IDE.

# engine = create_engine('sqlite:///db.sqlite3')
# metadata = MetaData()
# metadata.reflect(bind=engine)      # читает список таблиц и колонок из БД
#
# Base = automap_base(metadata=metadata)
# Base.prepare()                      # генерирует классы по прочитанным таблицам
# print(metadata.tables)
#
#
# User = Base.classes.users           # класс достаётся по ИМЕНИ ТАБЛИЦЫ, а не по имени класса
# user_1 = User(id=6, username='admin', age=20)
# print(user_1.id, user_1.username, user_1.age)


# --- Рабочий код: декларативный маппинг (VAR 2) с двумя таблицами ---

# Базовый класс: держит общий реестр metadata для всех моделей ниже.
class Base(DeclarativeBase):
    pass

# Таблица пользователей.
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)

# Вторая таблица — пока без связи (ForeignKey) с users; связи появятся на уроке 09.09.
class Address(Base):
    __tablename__ = 'addresses'
    # autoincrement=True указан явно, хотя для целочисленного PK это и так поведение по умолчанию.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(100))

# Подключение к файлу db.sqlite в текущем рабочем каталоге.
engine = create_engine('sqlite:///db.sqlite')

# Создаёт недостающие таблицы users и addresses.
Base.metadata.create_all(engine)

# Фабрика сессий.
Session = sessionmaker(bind=engine)


# Сессия открывается и сразу закрывается: в этом уроке важен только сам факт
# создания таблиц, никаких запросов пока не выполняется.
with Session() as session:
    pass
