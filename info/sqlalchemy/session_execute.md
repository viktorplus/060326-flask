# session.execute

```python
result = session.execute(stmt)
```

**Что это.** Выполняет запрос и возвращает строки целиком — объекты `Row`, похожие на именованные кортежи.

**Зачем.** Нужен, когда в выборке несколько колонок: агрегаты, группировки, выборка отдельных полей. `scalars` там оставил бы только первую колонку.

## Сигнатура

```python
session.execute(statement) -> Result
  .all()  .first()  .one()  .scalars()  либо итерирование
```

## Минимальный пример

```python
from sqlalchemy import func, select

query = select(User.username, func.count(User.id)).group_by(User.username)

rows = session.execute(query).all()
print(rows)                       # [('admin', 1), ('user2', 3), ...]

# К полям Row можно обращаться по имени
for row in session.execute(query):
    print(row.username, row.count)
```

## Типичные задачи

**Дать колонке имя и обращаться к ней по нему**

```python
query = (select(Address.city, func.count(Address.id).label('addr_count'))
         .group_by(Address.city))

for row in session.execute(query):
    print(row.city, row.addr_count)
```

**Несколько агрегатов одной строкой**

```python
query = select(func.count(User.id), func.min(User.age), func.max(User.age))
count, min_age, max_age = session.execute(query).one()
```

## Частые ошибки

- **Ожидать объекты модели.** `execute(select(User))` вернёт `Row`, внутри которых лежит `User`. Чтобы получить объекты напрямую, нужен `scalars`.
- **Распаковывать `Row` как обычный кортеж при одной колонке.** `row` останется кортежем из одного элемента — `row[0]` или `scalars()`.

## Где в репозитории

- `l07_orm_aggregates/app.py:79` — `result = session.execute(query).all()`
- `l07_orm_aggregates/app.py:91` — `result = session.execute(stmt).all()`
- `l05_orm_relationships/app.py:176` *(в закомментированном учебном блоке)* — `# result = session.execute(stmt).all()    # список КОРТЕЖЕЙ (Row), а не объектов`
- `l08_orm_loading/app.py:102` *(в закомментированном учебном блоке)* — `#     count_min_max = session.execute(query).one()   # .one() — ровно одна строка`

## См. также

[session_scalars](session_scalars.md), [func](func.md), [group_by](group_by.md)
