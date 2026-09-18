# .group_by()

```python
select(User.username, func.count(User.id)).group_by(User.username)
```

**Что это.** Группирует строки по значению колонки, чтобы применить к каждой группе агрегат.

**Зачем.** Вопросы вида «сколько адресов в каждом городе» решаются одним запросом вместо цикла с отдельным запросом на город.

## Сигнатура

```python
select(...).group_by(*columns)
```

## Минимальный пример

```python
from sqlalchemy import func, select

query = select(Address.city, func.count(Address.id).label('addr_count')).group_by(Address.city)

for row in session.execute(query):
    print(row.city, row.addr_count)
```

## Типичные задачи

**Группировка по нескольким колонкам**

```python
query = (select(User.age, Address.city, func.count(Address.id))
         .join(Address)
         .group_by(User.age, Address.city))
```

## Частые ошибки

- **Главное правило SQL: всё, что не под агрегатной функцией, обязано быть в `GROUP BY`.** PostgreSQL за нарушение ругается, SQLite — молча возвращает произвольное значение из группы.
- **Использовать `scalars`.** В выборке две колонки, и счётчик потеряется без ошибки. Нужен `execute`.
- **Фильтровать группы через `where`.** `WHERE` работает ДО группировки и агрегатов не видит. Для фильтра по агрегату нужен `having`.

## Где в репозитории

- `l07_orm_aggregates/app.py:76` — `query = select(User.username, func.count(User.id)).group_by(User.username)`
- `l07_orm_aggregates/app.py:90` — `stmt = select(user_aliase.username, func.count(user_aliase.id)).group_by(user_aliase.username)`
- `l08_orm_loading/app.py:108` *(в закомментированном учебном блоке)* — `#     query = select(Address.city, func.count(Address.id).label('addr_count')).group_by(Address.city`
- `l08_orm_loading/app.py:120` *(в закомментированном учебном блоке)* — `#                    .label('addr_count')).group_by(Address.city).having(func.count(Address.id) > 3)`

## См. также

[func](func.md), [having](having.md), [session_execute](session_execute.md)
