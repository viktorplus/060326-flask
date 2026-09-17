# Урок 11.09.26: стратегии загрузки связей (lazy), HAVING, подзапросы и JOIN.
# Главная тема — проблема N+1 запросов и способы её избежать.

# func нужен блоку с агрегатами и HAVING (ниже, в закомментированной части урока).
from sqlalchemy import create_engine, select, func, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


# Базовый класс моделей.
class Base(DeclarativeBase):
    pass


# Сторона «один».
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))

    # Без mapped_column(): тип колонки выводится напрямую из аннотации Mapped[int] -> INTEGER.
    # Вызов mapped_column() нужен только когда требуются параметры (primary_key, длина и т.п.).
    age: Mapped[int]

    # lazy='selectin' — отложенная, но пакетная загрузка: SQLAlchemy делает ОДИН
    # дополнительный запрос "SELECT ... FROM addresses WHERE user_id IN (...)"
    # сразу для всех загруженных пользователей.
    # Это и есть лекарство от N+1: без него на каждого пользователя шёл бы отдельный запрос.
    # Сравните с lazy='joined' в уроках 09.09/10.09 — там всё тянется одним JOIN-запросом.
    addresses: Mapped[list['Address']] = relationship(back_populates='user', lazy='selectin') # 1: M

    def __str__(self) -> str:
        return f'User: {self.name}; {self.age}'

    def __repr__(self) -> str:
        return f'User: {self.name}; {self.age}'


# Сторона «многие».
class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Внешний ключ: каждая строка addresses принадлежит ровно одному пользователю.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    city: Mapped[str] = mapped_column(String(50))

    # Обратная сторона связи; back_populates ссылается на User.addresses.
    user: Mapped["User"] = relationship(back_populates="addresses")

    # __str__ не переопределён — Python возьмёт для str() этот же __repr__.
    def __repr__(self) -> str:
        return f'Address: {self.city}'

# echo=True — печатать каждый выполненный SQL в консоль.
# Здесь это ключевой момент урока: видно, сколько именно запросов уходит в базу.
engine = create_engine('sqlite:///db.sqlite', echo=True)
# Создаём таблицы, если их ещё нет.
Base.metadata.create_all(engine)
# Фабрика сессий.
Session = sessionmaker(bind=engine)


# --- Наполнение базы (выполнено однажды, теперь закомментировано) ---
# Адреса передаются прямо в конструктор User списком: благодаря relationship
# SQLAlchemy сам расставит user_id и вставит строки в addresses (каскад save-update).
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
#     dave = User(name='Dave', age=17)          # пользователь вообще без адресов
#     eve = User(name='Eve', age=27, addresses=[
#         Address(city='Berlin'),
#     ])
#     session.add_all([alice, bob, carol, dave, eve])
#     session.commit()


# --- Разобранные на занятии агрегаты и подзапросы ---
# with Session() as session:
#     # all users
#     all_users = session.scalars(select(User))
#     print(*all_users, sep='\n')       # распаковка итератора в аргументы print
#     print('-' * 50)
#
#     # avg age of all users
#     # scalar() — для запроса, возвращающего одно значение
#     avg_age = session.scalar(select(func.avg(User.age)))
#     print(avg_age)
#     print('-' * 50)
#
#     # number of users, min age, max age
#     # Три агрегата в одном SELECT — результат одна строка из трёх колонок
#     query = select(func.count(User.id), func.min(User.age), func.max(User.age))
#     count_min_max = session.execute(query).one()   # .one() — ровно одна строка
#     print(count_min_max)
#     print('-' * 50)
#
#     # group by city - addresses in city
#     # .label('addr_count') даёт колонке имя, по которому к ней можно обратиться как row.addr_count
#     query = select(Address.city, func.count(Address.id).label('addr_count')).group_by(Address.city)
#     # city_addr_count = session.execute(query).all()
#     # print(city_addr_count, sep='\n')
#
#     # Итерация по Row: обращение к колонкам по имени вместо индексов row[0]/row[1]
#     for row in session.execute(query):
#         print(row.city, row.addr_count)
#
#     # get all cities where count(addr) > 3
#     # HAVING фильтрует УЖЕ СГРУППИРОВАННЫЕ строки; WHERE для агрегатов не подходит,
#     # потому что он применяется до группировки
#     query = select(Address.city, func.count(Address.id)
#                    .label('addr_count')).group_by(Address.city).having(func.count(Address.id) > 3)
#     cities_having = session.execute(query).all()
#     print(*cities_having, sep='\n')
#
#     # Скалярный подзапрос: результат одного SELECT используется внутри условия другого.
#     # .scalar_subquery() помечает запрос как «возвращает одно значение»,
#     # что позволяет сравнивать с ним колонку через >
#     avg_age_subq = select(func.avg(User.age)).scalar_subquery()
#     print(avg_age_subq)
#     print(type(avg_age_subq))
#     # «Все, кто старше среднего возраста» — одним запросом, без промежуточного round-trip
#     users = session.scalars(select(User).where(User.age > avg_age_subq)).all()
#     print(*users, sep='\n')


# --- Рабочий блок 1: демонстрация lazy='selectin' ---
with Session() as session:
    print('-' * 50)
    query = select(User)
    # Благодаря lazy='selectin' обращение к user.addresses НЕ порождает
    # по запросу на каждого пользователя: в логе echo=True видно ровно два SELECT —
    # один по users и один по addresses с условием IN.
    for user in session.scalars(query):
        print(user, user.addresses)

# --- Рабочий блок 2: JOIN как ФИЛЬТР, а не как загрузка данных ---
# Новая сессия = пустой кэш идентичности, поэтому запросы уйдут в базу заново.
with Session() as session:
    print('-' * 50)
    # .join(Address) — INNER JOIN: в выборку попадут только пользователи,
    # у которых есть хотя бы один адрес (Dave без адресов отсеется).
    # .distinct() убирает дубликаты: пользователь с двумя адресами иначе вернулся бы дважды.
    # ВАЖНО: join здесь лишь ограничивает набор строк; сами адреса всё равно
    # догружаются отдельным запросом из-за lazy='selectin'.
    # Чтобы join ещё и загружал связь, нужен .options(contains_eager(User.addresses)).
    query = select(User).join(Address).distinct()
    for user in session.scalars(query):
        print(user, user.addresses)
