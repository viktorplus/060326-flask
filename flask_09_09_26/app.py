from typing import Optional
import random

from sqlalchemy import create_engine, Integer, String, ForeignKey, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)
    # addresses: Mapped['Address'] = relationship(back_populates='user') # 1:1
    # addresses: Mapped[Optional['Address']] = relationship(back_populates='user')  # 1:1 or None
    addresses: Mapped[list['Address']] = relationship(back_populates='user') # 1: M

    def __str__(self) -> str:
        return f'User: {self.username}; {self.age}'

    def __repr__(self) -> str:
        return f'User: {self.username}; {self.age}'


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(100))

    # user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')

    # user: Mapped[User] = relationship(backref='addresses', uselist=False)




# from typing import List
# from sqlalchemy import Table, Column
#
# tags_association = Table(
#     'tags_association', Base.metadata,
#     Column('user_id', ForeignKey('users.id')),
#     Column('tag_id', ForeignKey('tags.id')),
# )
#
# class User(Base):
#     __tablename__ = 'users'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tags: Mapped[List["Tag"]] = relationship(secondary=tags_association, back_populates="users")
#
# class Tag(Base):
#     __tablename__ = 'tags'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     users: Mapped[List["User"]] = relationship(secondary=tags_association, back_populates="tags")





engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Create 1 User
# with Session() as session:
#     user = User(username=f'username{random.randint(1_000, 10_000)}', age=random.randint(20, 100))
#     session.add(user)
#     session.commit()


# with Session() as session:
#     users = [User(username=f'username{random.randint(1_000, 10_000)}', age=random.randint(20, 100))
#             for _ in range(20)]
#     session.add_all(users)
#     session.commit()

with Session() as session:
    user = session.get(User, 1)
    print(user)


    # stmt = select(User)
    # print(stmt)
    # print(type(stmt))
    #
    # result = session.scalars(stmt)
    # print(result)
    # print(type(result))
    #
    # result = list(session.scalars(stmt))
    # print(result)
    # print(type(result))

    for user in session.scalars(select(User)):
        print(user)

    user = session.get(User, 1)
    user.age = 135

    session.commit()

















