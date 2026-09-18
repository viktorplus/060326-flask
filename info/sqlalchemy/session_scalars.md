# session.scalars

```python
result = session.scalars(stmt)
```

**Что это.** Выполняет запрос и возвращает ПЕРВУЮ КОЛОНКУ каждой строки. Для `select(User)` — это готовые объекты `User`.

**Зачем.** В 90% случаев из запроса нужны именно объекты модели, а не кортежи. `scalars` избавляет от распаковки `row[0]` в каждом цикле.

## Сигнатура

```python
session.scalars(statement) -> ScalarResult
  .all()  .first()  .one()  .one_or_none()  либо итерирование
```

## Минимальный пример

```python
from sqlalchemy import select

stmt = select(User)

for user in session.scalars(stmt):          # ленивый обход
    print(user)

users = session.scalars(stmt).all()          # сразу список
```

## Типичные задачи

**Выборка с условием**

```python
query = select(User).where(User.age > 40)
adults = session.scalars(query).all()
```

## Частые ошибки

- **Использовать `scalars` для запроса с несколькими колонками.** `select(User.username, func.count(User.id))` через `scalars` вернёт только `username` — счётчик потеряется МОЛЧА, без ошибки. Для нескольких колонок нужен `execute`.
- **Повторно обходить результат.** `ScalarResult` — одноразовый итератор; нужен повторный проход — сохраните `.all()` в список.

## Где в репозитории

- `l05_orm_relationships/app.py:187` — `user_first = session.scalars(stmt).first()`
- `l05_orm_relationships/app.py:199` — `user_one = session.scalars(stmt.where(User.id == 1)).one()`
- `l05_orm_relationships/app.py:210` — `user_one = session.scalars(stmt.where(User.id == 1)).one_or_none()`
- `l05_orm_relationships/app.py:218` — `users_adult = session.scalars(query).all()`

## См. также

[session_execute](session_execute.md), [select](select.md), [first_one_all](first_one_all.md)
