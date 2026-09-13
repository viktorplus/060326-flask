# Урок 08.09.26 (часть 1): первое знакомство с SQLAlchemy ORM —
# декларативная модель, создание таблиц, сессия и вставка записи.

# Стандартный модуль логирования.
import logging

# create_engine — «точка входа» в БД: пул соединений + диалект конкретной СУБД.
# Column/String/Integer — старый (1.x) способ описания колонок, оставлен для сравнения ниже.
from sqlalchemy import create_engine, Column, String, Integer

# sessionmaker    — фабрика сессий (сессия = «рабочая единица», unit of work).
# DeclarativeBase — базовый класс для моделей в стиле SQLAlchemy 2.0.
# Mapped / mapped_column — современный типизированный способ описать колонку.
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# Настраиваем корневой логгер: без этого вызова сообщения никуда не выводятся.
logging.basicConfig(level=logging.DEBUG)

# Берём именно логгер 'sqlalchemy.engine' — через него SQLAlchemy печатает готовый SQL.
logger = logging.getLogger('sqlalchemy.engine')

# DEBUG показывает и сам SQL-запрос, и переданные в него параметры.
# Альтернатива тому же результату: create_engine(..., echo=True).
logger.setLevel(logging.DEBUG)



# Общий базовый класс. Он держит metadata — реестр всех описанных таблиц.
class Base(DeclarativeBase):
    pass


# Модель = таблица. Класс User соответствует строке таблицы 'users'.
class User(Base):
    # Обязательный атрибут: имя таблицы в БД.
    __tablename__ = 'users'

    # Старый синтаксис SQLAlchemy 1.x — оставлен закомментированным для сравнения.
    # Работает и сейчас, но не даёт подсказок типов в IDE.
    # id = Column(Integer, primary_key=True)
    # name = Column(String)
    # email = Column(String)

    # Современный синтаксис 2.0: тип колонки выводится из аннотации Mapped[...].
    # primary_key=True — первичный ключ; для int в SQLite он автоинкрементный.
    id: Mapped[int] = mapped_column(primary_key=True)
    # String(30) переопределяет тип по умолчанию и задаёт VARCHAR(30).
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)


# Строка подключения: sqlite:///<относительный путь к файлу>.
# Файл db.sqlite3 создастся в текущем рабочем каталоге при первом обращении.
engine = create_engine('sqlite:///db.sqlite3')

# Создаёт в БД все таблицы, описанные наследниками Base, которых там ещё нет.
# Существующие таблицы НЕ изменяются — под изменение схемы нужен Alembic.
Base.metadata.create_all(engine)

# Фабрика сессий, привязанная к этому движку. Session — класс, а не объект.
Session = sessionmaker(bind=engine)

# with гарантирует закрытие сессии (возврат соединения в пул) даже при исключении.
with Session() as session:
    # Явно задаём id=6 вместо автогенерации — при повторном запуске скрипта
    # это приведёт к IntegrityError (нарушение уникальности первичного ключа).
    # Пометка '#!' в исходнике — как раз об этом.
    new_user = User(id=6, username='admin', age=20) #!

    # add() только помечает объект как «новый» в сессии; SQL ещё не выполняется.
    session.add(new_user)

    # commit() выполняет INSERT и фиксирует транзакцию.
    # Без commit() все изменения будут отброшены при выходе из блока with.
    session.commit()
