# Практика 09.09.26 (часть 2): задания на SQLAlchemy — движок, логирование, модель.

# Column/String/Integer — «старые» Core-типы; из них реально используется только String/Integer.
# select — конструктор SELECT-запроса (стиль SQLAlchemy 2.0).
from sqlalchemy import create_engine, Column, String, Integer, select

# declarative_base — фабрика базового класса в стиле 1.x
# (в SQLAlchemy 2.0 предпочтительнее класс DeclarativeBase, как в других файлах проекта).
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column

import logging

"""Напишите код для создания движка SQLAlchemy с подключением к базе данных SQLite,
который будет располагаться в памяти, и настройте вывод логов всех операций с базой
данных на экран."""

# Настройка логирования: уровень INFO — именно на нём SQLAlchemy печатает SQL-запросы.
logging.basicConfig(level=logging.INFO)

# ЧАСТАЯ ОШИБКА, и раньше она была прямо здесь: считать, что одного basicConfig хватит.
# Рассуждение «логгер sqlalchemy.engine ничего своего не задаёт, значит унаследует INFO
# от корневого» звучит логично, но неверно: при импорте SQLAlchemy САМА выставляет своему
# логгеру 'sqlalchemy' уровень WARNING. Цепочка наследования обрывается на нём, и до
# корневого логгера дело не доходит — SQL в консоль не попадает. Причём ошибки никакой:
# скрипт отрабатывает молча, и кажется, что «логирование не включилось».
# Проверить самому: logging.getLogger('sqlalchemy').level  ->  30 (WARNING).
#
# Правильно — опустить уровень явно (ровно так же сделано в l04_orm_basics/app_1.py):
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Полностью эквивалентная альтернатива без возни с logging — create_engine(..., echo=True),
# как в l08_orm_loading/app.py.

# ОШИБКА, которая была здесь раньше: условие требует базу «в памяти», а в строке
# подключения стоял файл. Отличие в одном слове, но последствия разные: файловая
# база переживает перезапуск и копит мусор в рабочем каталоге, база в памяти живёт
# ровно столько, сколько живёт соединение. Так условию НЕ соответствует:
# engine = create_engine('sqlite:///base.db')

# Правильно: ':memory:' — специальное имя SQLite для базы в оперативной памяти.
engine = create_engine('sqlite:///:memory:')

# Базовый класс для моделей. Он же держит metadata со списком таблиц.
Base = declarative_base()

# Фабрика сессий, привязанная к движку. ВАЖНО для базы в памяти: она живёт, пока жив
# пул соединений этого движка, поэтому сессии обязаны создаваться от того же engine —
# иначе каждая получила бы свою пустую базу.
Session = sessionmaker(bind=engine)

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

# ВТОРАЯ ЧАСТЬ ЗАДАНИЯ — «вывод логов всех операций» — раньше не работала, и причина
# неочевидная: create_engine НЕ открывает соединение, он только настраивает пул.
# Пока никто не обратился к базе, SQLAlchemy нечего логировать, и экран остаётся пустым.
# Настройка логирования при этом выглядит правильной — легко решить, что «логи не включились».
# Достаточно любой реальной операции, чтобы лог ожил.
Base.metadata.create_all(engine)

# Сессия + запись: в логе появятся BEGIN, INSERT с параметрами и COMMIT.
with Session() as session:
    session.add(User(name='admin', age=20))
    session.commit()

    # SELECT на той же сессии — видно, что данные легли в базу.
    for user in session.scalars(select(User)):
        print(f'Из базы: id={user.id}, name={user.name}, age={user.age}')

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
