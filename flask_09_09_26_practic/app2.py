from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
import logging

"""Напишите код для создания движка SQLAlchemy с подключением к базе данных SQLite,
который будет располагаться в памяти, и настройте вывод логов всех операций с базой
данных на экран."""

logging.basicConfig(level=logging.INFO)
engine = create_engine('sqlite:///base.db')

Base = declarative_base()

""""Создайте модель User с полями:
● id (целочисленный тип, первичный ключ),
● name (строковый тип, длина до 50 символов),
● age (целочисленный тип).
"""""

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int] = mapped_column(Integer)

# ???
# class User(Base):
#  __tablename__ = 'users'
#  id = Column(Integer, primary_key=True)
#  name = Column(String(50))
#  age = Column(Integer)

# https://lms.itcareerhub.de/pluginfile.php/20091/mod_resource/content/1/Django_Pr2.pdf





