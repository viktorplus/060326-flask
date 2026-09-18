# select

```python
from sqlalchemy import select
```

**Что это.** Конструктор SELECT-запроса в стиле SQLAlchemy 2.0. Заменяет старый `session.query()`.

**Зачем.** `select()` строит объект запроса, но НЕ выполняет его. Запрос можно передавать, переиспользовать и достраивать — а выполнит его сессия.

## Сигнатура

```python
select(*entities) -> Select
  .where(...)  .order_by(...)  .group_by(...)  .having(...)
  .join(...)  .distinct()  .limit(n)  .offset(n)  .options(...)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `*entities` | — | — | Что выбирать: класс модели (`User`), отдельные колонки (`User.username`), агрегаты (`func.count(User.id)`) |

## Минимальный пример

```python
from sqlalchemy import select

stmt = select(User)
print(stmt)          # SELECT users.id, users.username, users.age FROM users
print(type(stmt))    # <class 'sqlalchemy.sql.selectable.Select'>

users = session.scalars(stmt).all()      # выполняет СЕССИЯ, не select
```

## Типичные задачи

**Выбрать только нужные колонки**

```python
stmt = select(User.username, User.age)       # два столбца -> нужен execute, не scalars
```

**Постраничная выдача**

```python
page, per_page = 2, 10
stmt = select(User).order_by(User.id).limit(per_page).offset((page - 1) * per_page)
```

**Достраивать запрос по условию — исходный объект не меняется**

```python
stmt = select(User)
if min_age is not None:
    stmt = stmt.where(User.age >= min_age)    # обязательно присвоить обратно!
if name:
    stmt = stmt.where(User.username.ilike(f'{name}%'))
```

## Частые ошибки

- **Ожидать, что `select()` что-то вернёт из базы.** Это только описание запроса. `print(stmt)` покажет SQL, но данных не будет, пока запрос не выполнит сессия.
- **`stmt.where(...)` без присваивания.** Методы возвращают НОВЫЙ объект, исходный не меняется. `stmt.where(User.age > 40)` сам по себе ничего не делает — нужно `stmt = stmt.where(...)`.
- **`scalars` для запроса с несколькими колонками** молча отбросит все, кроме первой.

## Где в репозитории

- `l05_orm_relationships/app.py:171` — `stmt = select(User)`
- `l05_orm_relationships/app.py:216` — `query = select(User).where(User.age > 40).where(User.age < 50)`
- `l05_orm_relationships/app.py:227` — `query = select(User).where(User.username.ilike('U%'))`
- `l05_orm_relationships/app.py:232` — `query = select(User).where(User.id.between(2, 4))`

## См. также

[where](where.md), [session_scalars](session_scalars.md), [order_by](order_by.md)
