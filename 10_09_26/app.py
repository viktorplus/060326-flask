from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy import select, label
from sqlalchemy import and_, or_, not_, desc
from sqlalchemy import func
from sqlalchemy.orm import aliased
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

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


with Session() as session:
    query = select(func.avg(User.age))
    result = session.scalar(query)
    print(result)

    query = select(User.username, func.count(User.id)).group_by(User.username)
    result = session.execute(query).all()
    print(result)

    user_aliase = aliased(User, name='user_aliase')

    stmt = select(user_aliase.username, func.count(user_aliase.id)).group_by(user_aliase.username)
    result = session.execute(stmt).all()
    print(result)








