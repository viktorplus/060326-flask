# .limit() / .offset()

```python
select(User).order_by(User.id).limit(10).offset(20)
```

**Что это.** Ограничение количества строк и пропуск первых N. Основа постраничной выдачи.

**Зачем.** Без ограничения запрос к большой таблице вытащит её целиком в память приложения.

## Сигнатура

```python
select(...).limit(n)
select(...).offset(n)
select(...).fetch(n)   # стандартный SQL-вариант
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``limit(n)`` | int | — | Сколько строк вернуть |
| ``offset(n)`` | int | — | Сколько первых строк пропустить |
| ``fetch(n)`` | int | — | То же, что `limit`, но синтаксисом стандарта SQL |

## Минимальный пример

```python
from sqlalchemy import select

# Вторая страница по 2 записи. order_by ОБЯЗАТЕЛЕН
page2 = select(User).order_by(User.id).limit(2).offset(2)
session.scalars(page2).all()
```

Вывод:

```
[U(Carol,30), U(Dave,17)]
```

## Типичные задачи

**Страница и общее число — два запроса**

```python
from sqlalchemy import func

page, per_page = 2, 10
items = session.scalars(
    select(User).order_by(User.id).limit(per_page).offset((page - 1) * per_page)).all()
total = session.scalar(select(func.count()).select_from(User))
```

**Постраничность по курсору — быстрее offset на больших таблицах**

```python
# Вместо offset запоминаем последний id и берём «то, что после него»
select(User).where(User.id > last_seen_id).order_by(User.id).limit(per_page)
```

## Частые ошибки

- **`limit` без `order_by`.** Порядок строк без сортировки не гарантирован вообще, и «первые 3» на разных запусках могут оказаться разными. На маленькой таблице кажется, что порядок стабилен, — до первой вставки или удаления.
- **Большой `offset` медленный.** База всё равно вычитывает и отбрасывает все пропускаемые строки: `offset(100000)` прочитает сто тысяч строк впустую. Для глубокой постраничности берут курсор по ключу.
- **`offset` без `limit` работает, `limit` без `offset` тоже** — но вместе они имеют смысл только при заданной сортировке.
- **Про `limit` с `joinedload` по коллекции беспокоиться не нужно.** Можно ожидать, что `JOIN` размножит строки и `LIMIT` обрежет не там. SQLAlchemy 2.0 это предусмотрел: он оборачивает ограниченный запрос в подзапрос и присоединяет связь уже к нему, поэтому `limit(3)` даёт ровно трёх родителей. Проверено.

## Где в репозитории

- `l09_orm_practice/app.py:128` — `query = select(User).limit(3)`
- `l09_orm_practice/app.py:138` — `query = select(User).order_by(User.name).limit(4)`

## См. также

[order_by](order_by.md), [select](select.md), [func](func.md), [lazy](lazy.md)
