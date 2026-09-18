# Домашняя работа 3: описать схему интернет-магазина на SQLAlchemy.
# Задания 1-5: движок, сессия, модель Product, модель Category, связь между ними.
#
# Относится к тому же блоку, что и l09_orm_practice. Теория по связям —
# в l05_orm_relationships.
#
# Запускать из каталога проекта:
#     cd p09_orm_homework
#     python app.py
#
# Скрипт создаёт shop.db в текущем каталоге и на этом заканчивается:
# блок сессии внизу оставлен пустым — задания на запросы в эту работу не входили.

from sqlalchemy import create_engine, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

# Decimal — точное десятичное число. Пара к Numeric на стороне БД: см. модель Product.
from decimal import Decimal


# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.

class Base(DeclarativeBase):
    pass


# Оба варианта рабочие, разница только в том, переживут ли данные завершение процесса.
# engine = create_engine('sqlite:///:memory:') # Для использования базы данных в памяти
engine = create_engine('sqlite:///shop.db') # Для использования базы данных в файле shop.db

# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.

Session = sessionmaker(bind=engine)

# Задача 3: Определите модель продукта Product со следующими типами колонок:

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Numeric(10, 2) + Mapped[Decimal] — правильная пара для денег.
    # 10 — всего значащих цифр, 2 — из них после запятой.
    # Float здесь не годится: двоичная дробь не представляет 0.1 точно,
    # и суммы «уезжают» на копейки (0.1 + 0.2 != 0.3).
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    # Вызов mapped_column() без аргументов можно опустить: тип выводится
    # прямо из аннотации, и `in_stock: Mapped[bool]` дало бы тот же результат.
    in_stock: Mapped[bool] = mapped_column()

    # Связь на уровне БАЗЫ: внешний ключ на таблицу categories.
    # В строке указывается имя ТАБЛИЦЫ, а не класса.
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # Связь на уровне КОДА: вместо числа category_id получаем готовый объект Category.
    category: Mapped["Category"] = relationship(back_populates="products")

# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # lazy="joined" — стратегия загрузки: товары приедут тем же запросом, одним
    # LEFT OUTER JOIN. Для стороны «многие» это удобно, но есть следствие:
    # JOIN размножает строки категории по числу её товаров, поэтому выборку
    # категорий придётся схлопывать — session.scalars(...).unique().
    # Без .unique() SQLAlchemy откажется отдавать результат:
    #     InvalidRequestError: The unique() method must be invoked on this Result
    # Для коллекций чаще берут lazy="selectin" — он делает два запроса без дублей.
    # Разбор стратегий — в info/sqlalchemy/lazy.md.
    products: Mapped[list[Product]] = relationship(back_populates="category", lazy="joined")

    description: Mapped[str] = mapped_column(String(255))

# Создаёт обе таблицы, если их ещё нет. Существующие не меняет.
Base.metadata.create_all(engine)

# Блок оставлен пустым: задания 1-5 заканчиваются на описании схемы.
# Примеры запросов к такой схеме — в l09_orm_practice и в справочнике info/sqlalchemy/.
with Session() as session:
    pass
