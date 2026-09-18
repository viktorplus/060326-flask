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
    case,
    create_engine,
    delete,
    desc,
    func,
    intersect,
    literal,
    not_,
    or_,
    select,
    union,
    union_all,
    update,
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

# ===========================================================================
# Сложные запросы. Дальше — не отдельные конструкции, а задачи, которые
# реально приходится решать, и то, как они выражаются в ORM.
# ===========================================================================

title(14, "exists: у кого есть адреса, а у кого нет")

with Session() as s:
    with_addr = select(User).where(User.addresses.any())
    without = select(User).where(~User.addresses.any())
    print("  с адресами :", [u.name for u in s.scalars(with_addr)])
    print("  без адресов:", [u.name for u in s.scalars(without)])
    print("  с адресом в Berlin:",
          [u.name for u in s.scalars(select(User).where(User.addresses.any(Address.city == "Berlin")))])

    print("\n  Почему не join: он вернёт Alice дважды, у неё два адреса.")
    print("    join           ->", [u.name for u in s.scalars(select(User).join(Address))])
    print("    any() (EXISTS) ->", [u.name for u in s.scalars(with_addr)])
    print("  EXISTS останавливается на первом совпадении и дубликатов не даёт.")

    print("\n  ЛОВУШКА: питоновский not вместо ~")
    try:
        select(User).where(not User.addresses.any())
    except TypeError as e:
        print("   ", e)

# ---------------------------------------------------------------------------
title(15, "case: разложить пользователей по возрастным группам")

with Session() as s:
    group = case(
        (User.age < 18, "ребёнок"),
        (User.age < 30, "молодой"),
        else_="взрослый",
    )
    rows = s.execute(select(User.name, group.label("группа")).order_by(User.name)).all()
    for name, g in rows:
        print(f"    {name:8} {g}")

    print("\n  Сколько человек в каждой группе — тем же выражением в group_by:")
    for g, n in s.execute(select(group.label("g"), func.count(User.id)).group_by(group)):
        print(f"    {g:10} {n}")

    print("\n  Условная сумма: сколько адресов в NY и сколько в остальных городах")
    ny, other = s.execute(select(
        func.sum(case((Address.city == "New York", 1), else_=0)).label("ny"),
        func.sum(case((Address.city != "New York", 1), else_=0)).label("other"),
    )).one()
    print(f"    NY: {ny}, остальные: {other}")

# ---------------------------------------------------------------------------
title(16, "subquery + join: топ пользователей по числу адресов")

with Session() as s:
    counts = (select(Address.user_id, func.count(Address.id).label("n"))
              .group_by(Address.user_id)
              .subquery())

    rows = s.execute(
        select(User.name, counts.c.n)
        .join(counts, User.id == counts.c.user_id)
        .order_by(counts.c.n.desc(), User.name)
    ).all()
    for name, n in rows:
        print(f"    {name:8} {n}")

    print("\n  Колонки подзапроса доступны ТОЛЬКО через .c —", "counts.c.n =", counts.c.n)

    print("\n  aliased(Model, subq) возвращает объекты, а не кортежи:")
    adults = aliased(User, select(User).where(User.age > 25).subquery())
    print("   ", [u.name for u in s.scalars(select(adults))])

# ---------------------------------------------------------------------------
title(17, "cte: именованный промежуточный набор и рекурсия")

with Session() as s:
    by_city = (select(Address.city, func.count(Address.id).label("n"))
               .group_by(Address.city)
               .cte("by_city"))
    print("  города, где больше одного адреса:")
    for city, n in s.execute(select(by_city.c.city, by_city.c.n).where(by_city.c.n > 1)):
        print(f"    {city:14} {n}")

    print("\n  Рекурсивный CTE — последовательность 1..5 без таблицы вообще:")
    base = select(literal(1).label("n")).cte("seq", recursive=True)
    seq = base.union_all(select(base.c.n + 1).where(base.c.n < 5))
    print("   ", s.execute(select(seq.c.n)).scalars().all())
    print("  Так же обходят деревья: категории, подчинённых, ветки комментариев.")
    print("  Без условия остановки (n < 5) запрос зациклится.")

# ---------------------------------------------------------------------------
title(18, "union / intersect: собрать несовместимые выборки в одну")

with Session() as s:
    young = select(User.name).where(User.age < 25)
    old = select(User.name).where(User.age > 40)

    print("  младше 25 ИЛИ старше 40:")
    print("   ", s.execute(union(young, old)).scalars().all())

    print("\n  union убирает дубликаты, union_all — нет:")
    print("    union(young, young)     ->", s.execute(union(young, young)).scalars().all())
    print("    union_all(young, young) ->", s.execute(union_all(young, young)).scalars().all())
    print("  union_all быстрее: базе не нужно сравнивать весь результат.")

    print("\n  intersect — кому ровно 30 И у кого есть адрес:")
    a30 = select(User.name).where(User.age == 30)
    withaddr = select(User.name).join(Address)
    print("   ", s.execute(intersect(a30, withaddr)).scalars().all())

# ---------------------------------------------------------------------------
title(19, "over: ранг внутри города, не схлопывая строки")

with Session() as s:
    rank = func.row_number().over(partition_by=Address.city, order_by=User.age.desc())
    print("  кто самый старший в каждом городе:")
    for city, name, age, r in s.execute(
        select(Address.city, User.name, User.age, rank.label("rank"))
        .join(User).order_by(Address.city, "rank")
    ):
        mark = "  <- первый" if r == 1 else ""
        print(f"    {city:14} {name:8} {age:3}  #{r}{mark}")

    print("\n  Отличие от group_by: строки остались на месте, добавилась колонка.")
    print("  Общее число рядом с каждой строкой — окно без partition_by:")
    for name, total in s.execute(select(User.name, func.count().over().label("total")).limit(3)):
        print(f"    {name:8} всего в выборке: {total}")

    print("\n  ЛОВУШКА: по окну нельзя фильтровать в WHERE — оно считается ПОСЛЕ.")
    print("  Нужен подзапрос: берём только тех, у кого rank = 1.")
    sub = select(Address.city, User.name, rank.label("rn")).join(User).subquery()
    print("   ", s.execute(select(sub.c.city, sub.c.name).where(sub.c.rn == 1)).all())

# ---------------------------------------------------------------------------
title(20, "limit / offset: постраничная выдача и её ловушка")

with Session() as s:
    total = s.scalar(select(func.count()).select_from(User))
    print(f"  всего пользователей: {total}")

    per_page = 2
    for page in (1, 2):
        q = select(User).order_by(User.id).limit(per_page).offset((page - 1) * per_page)
        print(f"    страница {page}: {[u.name for u in s.scalars(q)]}")

    print("\n  ЛОВУШКА: limit без order_by. Порядок строк не гарантирован вообще,")
    print("  и «первые два» на другой СУБД или после вставок окажутся другими.")
    print("    limit(2) без сортировки ->", [u.name for u in s.scalars(select(User).limit(2))])

    print("\n  Большой offset дорог: база вычитывает и выбрасывает всё, что пропускает.")
    print("  Для глубокой постраничности берут курсор по ключу:")
    last_id = 2
    q = select(User).where(User.id > last_id).order_by(User.id).limit(per_page)
    print("    после id=2 ->", [u.name for u in s.scalars(q)])

# ---------------------------------------------------------------------------
title(21, "bulk update / delete: одним запросом, без загрузки объектов")

with Session() as s:
    res = s.execute(update(User).where(User.age < 18).values(age=18))
    print(f"  update(age<18 -> 18): затронуто строк = {res.rowcount}")
    s.rollback()

    res = s.execute(delete(Address).where(Address.city == "Berlin"))
    print(f"  delete(city='Berlin'): затронуто строк = {res.rowcount}")
    s.rollback()
    print("  (оба отката сделаны, данные на месте)")

    print("\n  ГЛАВНОЕ ОТЛИЧИЕ от session.delete: каскады ORM НЕ срабатывают.")
    print("  delete(User) массовой формой оставит адреса с несуществующим user_id,")
    print("  даже если в relationship прописан cascade='all, delete-orphan'.")
    print("  Нужен каскад — либо session.delete(объект), либо ondelete='CASCADE' в базе.")

# ---------------------------------------------------------------------------
title(22, "session.delete: что делает каскад — и чего НЕ делает")

with Session() as s:
    alice = s.scalar(select(User).where(User.name == "Alice"))
    print(f"  у Alice адресов: {len(alice.addresses)}")
    print("  В этой модели relationship объявлен БЕЗ cascade. Удаляем родителя:")
    s.delete(alice)
    try:
        s.commit()
        print("    удалилось без ошибки")
    except IntegrityError as e:
        s.rollback()
        print(f"    IntegrityError: {str(e.orig)}")
        print("    ушедший SQL:  UPDATE addresses SET user_id=NULL WHERE addresses.id = ?")
        print()
        print("  ВОТ ЧТО ПРОИСХОДИТ. Каскад по умолчанию ('save-update, merge') при удалении")
        print("  родителя не удаляет детей, а ОТВЯЗЫВАЕТ их: ставит внешний ключ в NULL.")
        print("  Колонка user_id объявлена как NOT NULL — отсюда ошибка.")
        print("  Будь колонка nullable, ошибки бы не было, и в базе остались бы")
        print("  осиротевшие адреса без пользователя. Это хуже: ломается тихо.")


# Отдельная маленькая схема — показать, как это должно быть
class B2(DeclarativeBase):
    pass


class Parent(B2):
    __tablename__ = "parent"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    children: Mapped[list["Child"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan")


class Child(B2):
    __tablename__ = "child"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    parent: Mapped["Parent"] = relationship(back_populates="children")


e2 = create_engine("sqlite:///:memory:")
B2.metadata.create_all(e2)
S2 = sessionmaker(bind=e2)
with S2() as s:
    s.add(Parent(name="P", children=[Child(), Child(), Child()]))
    s.commit()

print()
print("  Та же операция, но с cascade='all, delete-orphan':")
with S2() as s:
    before = s.scalar(select(func.count()).select_from(Child))
    p = s.scalar(select(Parent))
    s.delete(p)
    s.commit()
    after = s.scalar(select(func.count()).select_from(Child))
    print(f"    детей в базе: {before} -> {after}  — ушли вместе с родителем")

    print()
    print("  Распространённое заблуждение: «после удаления объект трогать нельзя».")
    print(f"    p.id   -> {p.id}")
    print(f"    p.name -> {p.name}")
    print("  Читается без ошибки. Объект перешёл в detached, но уже загруженные значения")
    print("  остались при нём. DetachedInstanceError будет только при обращении к полю,")
    print("  которого в объекте нет: перечитать его неоткуда.")

print("\nГотово. База была в памяти — на диске ничего не осталось.")
