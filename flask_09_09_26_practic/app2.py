# Практика 09.09.26 (часть 2): задания на SQLAlchemy — движок, логирование, модель.

# Column/String/Integer — «старые» Core-типы; из них реально используется только String/Integer.
from sqlalchemy import create_engine, Column, String, Integer

# declarative_base — фабрика базового класса в стиле 1.x
# (в SQLAlchemy 2.0 предпочтительнее класс DeclarativeBase, как в других файлах проекта).
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

import logging

"""Напишите код для создания движка SQLAlchemy с подключением к базе данных SQLite,
который будет располагаться в памяти, и настройте вывод логов всех операций с базой
данных на экран."""

# Настройка логирования: уровень INFO — именно на нём SQLAlchemy печатает SQL-запросы.
# Логгер 'sqlalchemy.engine' наследует этот уровень от корневого, поэтому отдельно его
# настраивать не нужно. Эквивалентная альтернатива — create_engine(..., echo=True).
logging.basicConfig(level=logging.INFO)

# ЗАМЕЧАНИЕ по заданию: требовалась база «в памяти», то есть 'sqlite:///:memory:'.
# Здесь же указан файл base.db в текущем рабочем каталоге — база будет на диске.
engine = create_engine('sqlite:///base.db')

# Базовый класс для моделей. Он же держит metadata со списком таблиц.
Base = declarative_base()

""""Создайте модель User с полями:
● id (целочисленный тип, первичный ключ),
● name (строковый тип, длина до 50 символов),
● age (целочисленный тип).
"""""

# Модель пользователя.
class User(Base):
    # Имя таблицы в БД.
    __tablename__ = 'users'

    # Современный типизированный синтаксис: тип колонки выводится из Mapped[...].
    id: Mapped[int] = mapped_column(primary_key=True)
    # String(50) — VARCHAR(50), как требует условие задания.
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)

# ВНИМАНИЕ: Base.metadata.create_all(engine) здесь не вызывается,
# поэтому таблица users в base.db так и не создаётся, а сессия ни разу не открывается —
# движок к базе фактически не обращается и в лог ничего не попадает.

# ???
# Тот же класс в старом синтаксисе SQLAlchemy 1.x — через Column вместо Mapped/mapped_column.
# Результат в БД идентичный; разница только в подсказках типов для IDE и mypy.
# class User(Base):
#  __tablename__ = 'users'
#  id = Column(Integer, primary_key=True)
#  name = Column(String(50))
#  age = Column(Integer)

# Ссылка на методичку с условиями заданий.
# https://lms.itcareerhub.de/pluginfile.php/20091/mod_resource/content/1/Django_Pr2.pdf
