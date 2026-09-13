# Урок 09.09.26: связи между таблицами (relationship) и выборка данных через select().
# Основная тема второй половины файла — фильтры WHERE, операторы и сортировка.

# Optional используется в закомментированном варианте связи «1:1 или None».
from typing import Optional

# random нужен закомментированным блокам, которые наполняют таблицу тестовыми данными.
import random

# ForeignKey — внешний ключ, физическая связь на уровне БД.
from sqlalchemy import create_engine, Integer, String, ForeignKey

# select — конструктор SELECT-запроса (стиль SQLAlchemy 2.0, вместо старого session.query()).
from sqlalchemy import select

# Логические операторы для WHERE: И / ИЛИ / НЕ и сортировка по убыванию.
from sqlalchemy import and_, or_, not_, desc

# func — доступ к SQL-функциям (count, avg, min, max...). В этом файле не используется.
from sqlalchemy import func

# relationship — связь на уровне ORM (питоновские атрибуты-объекты, а не колонки).
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


# Общий базовый класс моделей.
class Base(DeclarativeBase):
    pass


# Сторона «один» в связи один-ко-многим.
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)

    # Варианты кардинальности связи — отличаются ТОЛЬКО аннотацией типа:
    # addresses: Mapped['Address'] = relationship(back_populates='user') # 1:1
    # addresses: Mapped[Optional['Address']] = relationship(back_populates='user')  # 1:1 or None

    # Mapped[list['Address']] => один пользователь -> много адресов.
    # back_populates='user' связывает этот атрибут с Address.user: изменение одной
    # стороны автоматически отражается на другой (двунаправленная связь).
    # 'Address' в кавычках — forward reference: класс объявлен ниже по файлу.
    addresses: Mapped[list['Address']] = relationship(back_populates='user') # 1: M

    # __str__ — «человеческое» представление (print, str()).
    def __str__(self) -> str:
        return f'User: {self.username}; {self.age}'

    # __repr__ — техническое представление; именно оно используется при печати СПИСКА объектов.
    # Здесь оба метода совпадают, чтобы вывод был одинаковым в любом случае.
    def __repr__(self) -> str:
        return f'User: {self.username}; {self.age}'


# Сторона «многие».
class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(100))

    # Тот же внешний ключ можно задать ссылкой на атрибут класса:
    # user_id: Mapped[int] = mapped_column(ForeignKey(User.id))

    # Строка 'users.id' — это <имя_таблицы>.<имя_колонки>, а не <имя_класса>.<атрибут>.
    # Вариант со строкой не требует, чтобы класс User был уже определён.
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Обратная сторона связи. lazy='joined' — стратегия загрузки:
    # связанный User подтягивается сразу тем же запросом через LEFT OUTER JOIN,
    # что избавляет от проблемы N+1 запросов.
    user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')

    # Альтернатива back_populates: backref создаёт обратный атрибут User.addresses
    # автоматически, без объявления его в классе User.
    # user: Mapped[User] = relationship(backref='addresses', uselist=False)




# --- Связь «многие-ко-многим» (many-to-many) — материал для справки ---
# Требует третью, ассоциативную таблицу, которая хранит пары (user_id, tag_id).
# Она описывается через Core-объект Table, а не через класс-модель,
# и подключается к relationship параметром secondary=...

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




# Подключение к файлу БД в текущем рабочем каталоге.
engine = create_engine('sqlite:///db.sqlite')

# Создаём таблицы, если их ещё нет.
Base.metadata.create_all(engine)

# Фабрика сессий.
Session = sessionmaker(bind=engine)


# --- Наполнение базы тестовыми данными (выполнялось один раз, теперь закомментировано) ---

# Create 1 User
# with Session() as session:
#     user = User(username=f'username{random.randint(1_000, 10_000)}', age=random.randint(20, 100))
#     session.add(user)
#     session.commit()


# Массовая вставка: add_all принимает список объектов сразу.
# with Session() as session:
#     users = [User(username=f'username{random.randint(1_000, 10_000)}', age=random.randint(20, 100))
#             for _ in range(20)]
#     session.add_all(users)
#     session.commit()

# Чтение и обновление:
# with Session() as session:
#     user = session.get(User, 1)     # выборка по первичному ключу
#     print(user)
#
#
#     # Разница между объектом запроса, курсором и готовым списком:
#     # stmt = select(User)
#     # print(stmt)                   # сам SQL-текст
#     # print(type(stmt))             # Select — запрос ещё НЕ выполнен
#     #
#     # result = session.scalars(stmt)
#     # print(result)
#     # print(type(result))           # ScalarResult — «курсор», итератор по строкам
#     #
#     # result = list(session.scalars(stmt))
#     # print(result)
#     # print(type(result))           # обычный list с объектами User
#
#     for user in session.scalars(select(User)):
#         print(user)
#
#     user = session.get(User, 1)
#     user.age = 135                  # ORM отслеживает изменение атрибута...
#
#     session.commit()                # ...и на commit генерирует UPDATE



# --- Рабочий блок: способы получить данные и фильтры WHERE ---
with Session() as session:
    # Базовый запрос «взять все строки users». Пока это только объект-описание запроса.
    stmt = select(User)

    # Три варианта выполнения одного и того же запроса:
    # result = session.scalars(stmt).all()    # список объектов User
    # result = session.scalars(stmt)          # ленивый итератор
    # result = session.execute(stmt).all()    # список КОРТЕЖЕЙ (Row), а не объектов

    # .first() — первая строка или None, если результат пуст.
    # ВНИМАНИЕ: если таблица пуста, обращение к user_first.id упадёт с AttributeError.
    user_first = session.scalars(stmt).first()
    print(user_first, user_first.id, user_first.username, user_first.age)

    # .where(...) возвращает НОВЫЙ объект запроса, исходный stmt не меняется.
    # == внутри where — это не сравнение Python, а построение SQL-условия "id = 1".
    # .one() требует ровно одну строку: 0 строк -> NoResultFound, 2+ -> MultipleResultsFound.
    user_one = session.scalars(stmt.where(User.id==1)).one()
    print(user_one, user_one.id, user_one.username, user_one.age)

    # session.get ищет по первичному ключу и возвращает None, если записи нет
    # (исключение не бросается — в отличие от .one()).
    user_one_get = session.get(User, 100000)
    print(user_one_get)

    # .one_or_none() — компромисс: 0 строк -> None, 1 -> объект, 2+ -> исключение.
    user_one = session.scalars(stmt.where(User.id == 1)).one_or_none()
    # Поэтому результат обязательно проверяем перед использованием.
    if user_one:
        print(user_one, user_one.id, user_one.username, user_one.age)

    # Два .where() подряд склеиваются через AND: age > 40 AND age < 50.
    query = select(User).where(User.age > 40).where(User.age < 50)
    # .all() материализует результат в обычный список.
    users_adult = session.scalars(query).all()
    # Список печатается через __repr__ каждого элемента.
    print(users_adult)

    # Разделитель для читаемости вывода в консоли.
    print('*' * 20)

    # ilike — сравнение по шаблону БЕЗ учёта регистра ('%' = любая последовательность символов).
    # like — та же операция, но с учётом регистра.
    query = select(User).where(User.username.ilike('U%'))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # between(a, b) -> SQL BETWEEN: границы ВКЛЮЧАЮТСЯ (2 <= id <= 4).
    query = select(User).where(User.id.between(2, 4))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # Список значений для проверки вхождения.
    names = ['username6132', 'username9452', 'username4585']

    # in_() -> SQL IN (...). Подчёркивание в имени — потому что in зарезервировано в Python.
    query = select(User).where(User.username.in_(names))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # or_(...) объединяет условия через OR. Питоновский or здесь использовать НЕЛЬЗЯ —
    # он вернул бы одно из выражений, а не построил SQL-условие.
    query = select(User).where(or_(User.username.ilike('U%'), User.username.ilike('A%')))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # Тот же OR, но по числовому полю: моложе 20 ИЛИ старше 50.
    query = select(User).where(or_(User.age < 20, User.age > 50))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # not_(...) -> SQL NOT: инвертирует условие (age > 40 становится age <= 40).
    query = select(User).where(not_(User.age > 40))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # ORDER BY по возрастанию — направление по умолчанию.
    query = select(User).order_by(User.age)
    users_adult = session.scalars(query).all()
    print(users_adult)

    # desc(...) -> ORDER BY age DESC (по убыванию).
    query = select(User).order_by(desc(User.age))
    users_adult = session.scalars(query).all()
    print(users_adult)

    # Сортировка по нескольким ключам: сначала возраст по убыванию,
    # а внутри одинакового возраста — имя по возрастанию.
    query = select(User).order_by(desc(User.age), User.username)
    users_adult = session.scalars(query).all()
    print(users_adult)
