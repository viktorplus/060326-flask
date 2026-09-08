from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry, Mapped, mapped_column
from sqlalchemy.ext.automap import automap_base

# VAR 1

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

# engine = create_engine('sqlite:///db.sqlite3')
# metadata = MetaData()
# metadata.reflect(bind=engine)
#
# Base = automap_base(metadata=metadata)
# Base.prepare()
# print(metadata.tables)
#
#
# User = Base.classes.users
# user_1 = User(id=6, username='admin', age=20)
# print(user_1.id, user_1.username, user_1.age)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)

class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(100))

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


with Session() as session:
    pass







