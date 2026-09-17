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

# Эта строка ОБЯЗАТЕЛЬНА, и вот почему: при импорте SQLAlchemy сама выставляет своему
# логгеру 'sqlalchemy' уровень WARNING. Наследование уровня обрывается на нём, поэтому
# один только basicConfig(level=DEBUG) выше SQL в консоль не выведет — и это выглядит
# так, будто «логирование не включилось». Разбор той же ошибки — в l06_practice/app2.py.
#
# DEBUG показывает и сам SQL-запрос, и переданные в него параметры (INFO — только запрос).
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
    # ЧАСТАЯ ОШИБКА: задать первичный ключ руками.
    # Такая строка отработает ОДИН раз, а на втором запуске упадёт с IntegrityError
    # (UNIQUE constraint failed: users.id) — запись с id=6 уже в базе. Коварство в том,
    # что «первый раз всё получилось», и проблема вылезает позже. Так НЕ надо:
    # new_user = User(id=6, username='admin', age=20)

    # Правильно: id не указываем вовсе. Колонка объявлена как primary_key,
    # SQLite подставит следующий свободный номер сам, и скрипт можно запускать
    # сколько угодно раз подряд.
    new_user = User(username='admin', age=20)

    # add() только помечает объект как «новый» в сессии; SQL ещё не выполняется.
    session.add(new_user)

    # commit() выполняет INSERT и фиксирует транзакцию.
    # Без commit() все изменения будут отброшены при выходе из блока with.
    session.commit()
