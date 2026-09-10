from typing import Optional
import random

from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy import select
from sqlalchemy import and_, or_, not_, desc
from sqlalchemy import func
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

# with Session() as session:
#     user = session.get(User, 1)
#     print(user)
#
#
#     # stmt = select(User)
#     # print(stmt)
#     # print(type(stmt))
#     #
#     # result = session.scalars(stmt)
#     # print(result)
#     # print(type(result))
#     #
#     # result = list(session.scalars(stmt))
#     # print(result)
#     # print(type(result))
#
#     for user in session.scalars(select(User)):
#         print(user)
#
#     user = session.get(User, 1)
#     user.age = 135
#
#     session.commit()



with Session() as session:
    stmt = select(User)
    # result = session.scalars(stmt).all()
    # result = session.scalars(stmt)
    # result = session.execute(stmt).all()

    user_first = session.scalars(stmt).first()
    print(user_first, user_first.id, user_first.username, user_first.age)

    user_one = session.scalars(stmt.where(User.id==1)).one()
    print(user_one, user_one.id, user_one.username, user_one.age)

    user_one_get = session.get(User, 100000)
    print(user_one_get)

    user_one = session.scalars(stmt.where(User.id == 1)).one_or_none()
    if user_one:
        print(user_one, user_one.id, user_one.username, user_one.age)

    query = select(User).where(User.age > 40).where(User.age < 50)
    users_adult = session.scalars(query).all()
    print(users_adult)
    print('*' * 20)
    query = select(User).where(User.username.ilike('U%'))
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).where(User.id.between(2, 4))
    users_adult = session.scalars(query).all()
    print(users_adult)

    names = ['username6132', 'username9452', 'username4585']

    query = select(User).where(User.username.in_(names))
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).where(or_(User.username.ilike('U%'), User.username.ilike('A%')))
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).where(or_(User.age < 20, User.age > 50))
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).where(not_(User.age > 40))
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).order_by(User.age)
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).order_by(desc(User.age))
    users_adult = session.scalars(query).all()
    print(users_adult)

    query = select(User).order_by(desc(User.age), User.username)
    users_adult = session.scalars(query).all()
    print(users_adult)


















