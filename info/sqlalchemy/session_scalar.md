# session.scalar

```python
value = session.scalar(stmt)
```

**Что это.** Выполняет запрос и возвращает ОДНО значение — первую колонку первой строки.

**Зачем.** Идеален для одиночного агрегата: среднее, количество, максимум. Не нужно ни распаковывать строку, ни звать `.first()`.

## Сигнатура

```python
session.scalar(statement) -> Any | None
```

## Минимальный пример

```python
from sqlalchemy import func, select

avg_age = session.scalar(select(func.avg(User.age)))
print(avg_age)
```

Вывод:

```
71.95238095238095
```

## Типичные задачи

**Проверить, есть ли вообще записи**

```python
total = session.scalar(select(func.count(User.id)))
if not total:
    print('таблица пуста')
```

## Частые ошибки

- **Путать `scalar` и `scalars`.** `scalar` (без s) — одно значение; `scalars` (с s) — последовательность значений.
- **`func.avg` на пустой таблице возвращает `None`, а не 0.** Арифметика с результатом без проверки даст `TypeError`.
- **Использовать для запроса с несколькими колонками** — вернётся только первая, молча.

## Где в репозитории

- `l05_orm_relationships/app.py:187` — `user_first = session.scalars(stmt).first()`
- `l05_orm_relationships/app.py:199` — `user_one = session.scalars(stmt.where(User.id == 1)).one()`
- `l05_orm_relationships/app.py:210` — `user_one = session.scalars(stmt.where(User.id == 1)).one_or_none()`
- `l05_orm_relationships/app.py:218` — `users_adult = session.scalars(query).all()`

## См. также

[session_scalars](session_scalars.md), [func](func.md), [session_execute](session_execute.md)
