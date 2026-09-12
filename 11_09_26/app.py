from sqlalchemy import create_engine, select, func, desc, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, aliased


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]
    addresses: Mapped[list['Address']] = relationship(back_populates='user', lazy='selectin') # 1: M

    def __str__(self) -> str:
        return f'User: {self.name}; {self.age}'

    def __repr__(self) -> str:
        return f'User: {self.name}; {self.age}'


class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    city: Mapped[str] = mapped_column(String(50))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f'Address: {self.city}'

engine = create_engine('sqlite:///db.sqlite', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# with Session() as session:
#     alice = User(name='Alice', age=30, addresses=[
#         Address(city='New York'),
#         Address(city='Los Angeles'),
#     ])
#     bob = User(name='Bob', age=22, addresses=[
#         Address(city='New York'),
#     ])
#     carol = User(name='Carol', age=30, addresses=[
#         Address(city='Los Angeles'),
#     ])
#     dave = User(name='Dave', age=17)
#     eve = User(name='Eve', age=27, addresses=[
#         Address(city='Berlin'),
#     ])
#     session.add_all([alice, bob, carol, dave, eve])
#     session.commit()


# with Session() as session:
#     # all users
#     all_users = session.scalars(select(User))
#     print(*all_users, sep='\n')
#     print('-' * 50)
#
#     # avg age of all users
#     avg_age = session.scalar(select(func.avg(User.age)))
#     print(avg_age)
#     print('-' * 50)
#
#     # number of users, min age, max age
#     query = select(func.count(User.id), func.min(User.age), func.max(User.age))
#     count_min_max = session.execute(query).one()
#     print(count_min_max)
#     print('-' * 50)
#
#     # group by city - addresses in city
#     query = select(Address.city, func.count(Address.id).label('addr_count')).group_by(Address.city)
#     # city_addr_count = session.execute(query).all()
#     # print(city_addr_count, sep='\n')
#
#     for row in session.execute(query):
#         print(row.city, row.addr_count)
#
#     # get all cities where count(addr) > 3
#     query = select(Address.city, func.count(Address.id)
#                    .label('addr_count')).group_by(Address.city).having(func.count(Address.id) > 3)
#     cities_having = session.execute(query).all()
#     print(*cities_having, sep='\n')
#
#     avg_age_subq = select(func.avg(User.age)).scalar_subquery()
#     print(avg_age_subq)
#     print(type(avg_age_subq))
#     users = session.scalars(select(User).where(User.age > avg_age_subq)).all()
#     print(*users, sep='\n')


with Session() as session:
    print('-' * 50)
    query = select(User)
    for user in session.scalars(query):
        print(user, user.addresses)

with Session() as session:
    print('-' * 50)
    query = select(User).join(Address).distinct()
    for user in session.scalars(query):
        print(user, user.addresses)





