# -*- coding: utf-8 -*-
"""Запускаемые примеры к справочнику SQLAlchemy 2.0.

    cd info/sqlalchemy
    python examples.py

База создаётся в оперативной памяти (sqlite:///:memory:) и наполняется заново
при каждом запуске — на диске ничего не появляется.
"""
import logging

from sqlalchemy import (
    ForeignKey,
    String,
    create_engine,
    desc,
    func,
    not_,
    or_,
    select,
)
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    aliased,
    contains_eager,
    mapped_column,
    relationship,
    selectinload,
    sessionmaker,
)


def title(n: int, text: str) -> None:
    print(f"\n{'=' * 70}\n{n}. {text}\n{'=' * 70}")


# ---------------------------------------------------------------------------
# Модели
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]                       # вызов не нужен: тип ясен из аннотации
    nickname: Mapped[str | None]           # NULL разрешён

    # lazy='select' — стратегия ПО УМОЛЧАНИЮ, она же источник проблемы N+1
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User({self.name}, {self.age})"


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address({self.city})"


engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

with Session() as s:
    s.add_all([
        User(name="Alice", age=30, addresses=[Address(city="New York"), Address(city="Los Angeles")]),
        User(name="Bob", age=22, addresses=[Address(city="New York")]),
        User(name="Carol", age=30, addresses=[Address(city="Los Angeles")]),
        User(name="Dave", age=17),                       # без адресов — важен для join
        User(name="Eve", age=27, addresses=[Address(city="Berlin")]),
    ])
    s.commit()

# ---------------------------------------------------------------------------
title(1, "create_engine НЕ открывает соединение — в логе поэтому пусто")

logging.basicConfig(level=logging.INFO)
print("уровень логгера 'sqlalchemy' сразу после импорта:",
      logging.getLevelName(logging.getLogger("sqlalchemy").level))
print("-> SQLAlchemy сама поставила себе WARNING, и наследование от корневого логгера")
print("   обрывается на нём. Одного basicConfig(level=INFO) НЕ ХВАТИТ.")

quiet = create_engine("sqlite:///:memory:")
print("\ncreate_engine выполнен, вывода выше нет: соединение не открывалось.")
print("Логгер включается явно: logging.getLogger('sqlalchemy.engine').setLevel(INFO)")

# ---------------------------------------------------------------------------
title(2, "select строит запрос, но НЕ выполняет его")

stmt = select(User)
print("тип:", type(stmt).__name__)
print("SQL:", str(stmt).replace("\n", " "))
print("-> данных нет: выполняет СЕССИЯ, а не select")

# ---------------------------------------------------------------------------
title(3, "scalars против execute: куда девается вторая колонка")

with Session() as s:
    one_col = select(User.name)
    two_col = select(User.name, User.age)

    print("scalars(select(User.name))       ->", s.scalars(one_col).all())
    print("scalars(select(User.name, age))  ->", s.scalars(two_col).all())
    print("  ^ ЛОВУШКА: возраст потерялся МОЛЧА, ошибки нет")
    print("execute(select(User.name, age))  ->", s.execute(two_col).all())

# ---------------------------------------------------------------------------
title(4, "first / one / one_or_none / all — что при нуле строк")

with Session() as s:
    empty = select(User).where(User.name == "Такого нет")

    print("first()        ->", s.scalars(empty).first(), "(None, исключения нет)")
    print("one_or_none()  ->", s.scalars(empty).one_or_none())
    print("all()          ->", s.scalars(empty).all(), "(пустой список)")
    try:
        s.scalars(empty).one()
    except NoResultFound as e:
        print("one()          -> NoResultFound:", e)

    print("\nЛОВУШКА, из-за которой падал l05: обращение к полю сразу после first()")
    user = s.scalars(empty).first()
    try:
        print(user.id)
    except AttributeError as e:
        print("   ", e)
    print("    правильно: if user: ...")

    print("\nsession.get по первичному ключу:")
    print("  get(User, 1)      ->", s.get(User, 1))
    print("  get(User, 100000) ->", s.get(User, 100000), "(None, а не исключение)")

# ---------------------------------------------------------------------------
title(5, "Операторы WHERE")

with Session() as s:
    base = select(User)
    checks = [
        ("age > 25",                 base.where(User.age > 25)),
        ("два .where() -> AND",      base.where(User.age > 20).where(User.age < 30)),
        ("between(22, 30)",          base.where(User.age.between(22, 30))),
        ("name.ilike('a%')",         base.where(User.name.ilike("a%"))),
        ("name.like('a%')",          base.where(User.name.like("a%"))),
        ("name.in_([...])",          base.where(User.name.in_(["Alice", "Eve"]))),
        ("or_(age<20, age>29)",      base.where(or_(User.age < 20, User.age > 29))),
        ("not_(age > 25)",           base.where(not_(User.age > 25))),
        ("nickname.is_(None)",       base.where(User.nickname.is_(None))),
    ]
    for label_text, q in checks:
        print(f"  {label_text:24} -> {[u.name for u in s.scalars(q)]}")

    print("\nЛОВУШКА: питоновские and / or / not вместо and_() / or_() / not_()")
    for label_text, fn in [("(age > 20) and (age < 30)", lambda: (User.age > 20) and (User.age < 30)),
                           ("(age < 20) or (age > 30)", lambda: (User.age < 20) or (User.age > 30)),
                           ("not (age > 40)", lambda: not (User.age > 40))]:
        try:
            print(f"   {label_text:26} -> вернул {fn()}")
        except TypeError as e:
            print(f"   {label_text:26} -> TypeError: {e}")
    print("   -> and/or/not требуют привести условие к bool, а условие SQL не истина и не ложь.")
    print("      SQLAlchemy 2.0 это запрещает — и хорошо: ошибка видна сразу, а не превращается")
    print("      в молча неверный фильтр.")

# ---------------------------------------------------------------------------
title(6, "order_by")

with Session() as s:
    print("  по возрастанию :", [u.name for u in s.scalars(select(User).order_by(User.age))])
    print("  по убыванию    :", [u.name for u in s.scalars(select(User).order_by(desc(User.age)))])
    print("  age desc, name :", [(u.name, u.age) for u in
                                 s.scalars(select(User).order_by(desc(User.age), User.name))])

# ---------------------------------------------------------------------------
title(7, "func, group_by, having, label")

with Session() as s:
    print("  средний возраст :", s.scalar(select(func.avg(User.age))))
    count, min_age, max_age = s.execute(
        select(func.count(User.id), func.min(User.age), func.max(User.age))).one()
    print(f"  count/min/max   : {count} / {min_age} / {max_age}")

    q = select(Address.city, func.count(Address.id).label("addr_count")).group_by(Address.city)
    print("  адресов по городам:")
    for row in s.execute(q):
        print(f"    {row.city:14} {row.addr_count}   <- обращение по имени из label()")

    q_having = q.having(func.count(Address.id) > 1)
    print("  где больше одного (HAVING):", s.execute(q_having).all())

    print("\n  WHERE против HAVING: WHERE — до группировки, HAVING — после.")
    print("  func.avg на пустой выборке возвращает:",
          s.scalar(select(func.avg(User.age)).where(User.age > 1000)), "<- None, а не 0")

# ---------------------------------------------------------------------------
title(8, "aliased: одна таблица дважды в одном запросе")

with Session() as s:
    u1 = aliased(User, name="u1")
    u2 = aliased(User, name="u2")
    pairs = s.execute(
        select(u1.name, u2.name)
        .join(u2, u1.age == u2.age)
        .where(u1.id < u2.id)          # без этого будут пары с самим собой и дубли
    ).all()
    print("  пары пользователей одного возраста:", pairs)
    print("  -> без псевдонимов такой запрос выразить нельзя")

# ---------------------------------------------------------------------------
title(9, "join — это ФИЛЬТР, а не загрузка связи")

with Session() as s:
    without = [u.name for u in s.scalars(select(User))]
    with_join = [u.name for u in s.scalars(select(User).join(Address))]
    with_distinct = [u.name for u in s.scalars(select(User).join(Address).distinct())]
    with_outer = [u.name for u in s.scalars(select(User).outerjoin(Address).distinct())]

    print("  select(User)                      ->", without)
    print("  .join(Address)                    ->", with_join)
    print("     ^ Alice дважды: у неё два адреса. Dave исчез: адресов нет")
    print("  .join(Address).distinct()         ->", with_distinct)
    print("  .outerjoin(Address).distinct()    ->", with_outer, " <- Dave вернулся")

# ---------------------------------------------------------------------------
title(10, "Проблема N+1 и стратегии загрузки — считаем запросы")

counter = {"n": 0}


@__import__("sqlalchemy").event.listens_for(engine, "before_cursor_execute")
def _count(conn, cursor, statement, parameters, context, executemany):
    counter["n"] += 1


def count_queries(label_text, options=None):
    counter["n"] = 0
    with Session() as s:                      # новая сессия: пустой кэш объектов
        q = select(User)
        if options is not None:
            q = q.options(options)
        for user in s.scalars(q):
            _ = user.addresses                # обращение к связи
    print(f"  {label_text:34} запросов: {counter['n']}")


count_queries("lazy='select' (по умолчанию)")
count_queries("options(selectinload(...))", selectinload(User.addresses))
print("  -> 6 запросов против 2: один за пользователями + по одному на каждого из пяти.")
print("     Это и есть N+1. На пяти строках незаметно, на пяти тысячах — катастрофа.")

counter["n"] = 0
with Session() as s:
    result = s.scalars(select(User).join(Address).options(contains_eager(User.addresses)))
    # .unique() обязателен: joined eager load по КОЛЛЕКЦИИ размножает строки,
    # и SQLAlchemy требует явно схлопнуть дубли, иначе InvalidRequestError
    for user in result.unique():
        _ = user.addresses
print(f"  {'join + contains_eager':34} запросов: {counter['n']}  <- join ЕЩЁ И наполнил коллекцию")

# ---------------------------------------------------------------------------
title(11, "scalar_subquery: пользователи старше среднего")

with Session() as s:
    avg_subq = select(func.avg(User.age)).scalar_subquery()
    older = s.scalars(select(User).where(User.age > avg_subq)).all()
    print("  средний возраст:", s.scalar(select(func.avg(User.age))))
    print("  старше среднего:", [u.name for u in older])
    print("  -> одним запросом, без гонки между двумя обращениями к базе")

# ---------------------------------------------------------------------------
title(12, "IntegrityError: почему нельзя задавать id вручную")

with Session() as s:
    s.add(User(id=999, name="Manual", age=40))
    s.commit()
    print("  первая вставка с id=999: прошла")

with Session() as s:
    try:
        s.add(User(id=999, name="Manual", age=40))
        s.commit()
    except IntegrityError as e:
        s.rollback()                          # без rollback сессия непригодна
        print("  вторая вставка:", str(e.orig))
        print("  -> именно эта ошибка была в l04_orm_basics/app_1.py")

with Session() as s:
    s.add(User(name="Auto", age=41))          # id не указываем
    s.add(User(name="Auto", age=42))
    s.commit()
    autos = s.scalars(select(User).where(User.name == "Auto")).all()
    print("  без указания id:", [(u.id, u.name) for u in autos], "<- можно запускать сколько угодно")

# ---------------------------------------------------------------------------
title(13, "add() не выполняет SQL, commit() — выполняет")

with Session() as s:
    u = User(name="Flush", age=50)
    s.add(u)
    print("  после add()   : id =", u.id, "(ещё None — база его не присвоила)")
    s.flush()
    print("  после flush() : id =", u.id, "(INSERT ушёл, транзакция ещё открыта)")
    s.commit()
    print("  после commit(): id =", u.id, "(зафиксировано)")

print("\nГотово. База была в памяти — на диске ничего не осталось.")
