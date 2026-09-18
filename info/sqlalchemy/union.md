# union / union_all

```python
from sqlalchemy import union, union_all, intersect, except_
```

**Что это.** Объединение результатов нескольких запросов в один набор строк.

**Зачем.** Когда данные лежат в разных местах или отбираются по несовместимым условиям, а получить их нужно одним списком.

## Сигнатура

```python
union(q1, q2, ...)        # объединение БЕЗ дубликатов
union_all(q1, q2, ...)    # объединение С дубликатами, быстрее
intersect(q1, q2)         # только строки, которые есть в обоих
except_(q1, q2)           # строки первого, которых нет во втором
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``union`` | — | — | Убирает дубликаты — значит, сортирует или хеширует весь результат |
| ``union_all`` | — | — | Дубликаты оставляет. **Быстрее**, и чаще всего нужен именно он |
| ``intersect`` | — | — | Пересечение |
| ``except_`` | — | — | Разность. Подчёркивание — потому что `except` зарезервировано в Python |

## Минимальный пример

```python
from sqlalchemy import select, union, union_all, intersect

young = select(User.name).where(User.age < 25)
old = select(User.name).where(User.age > 40)

session.execute(union(young, old)).scalars().all()
```

Вывод:

```
['Bob', 'Dave', 'Frank']
```

## Типичные задачи

**union_all не убирает повторы**

```python
session.execute(union_all(young, young)).scalars().all()
# ['Bob', 'Dave', 'Bob', 'Dave']
```

**Пересечение: кому 30 лет И у кого есть адрес**

```python
a30 = select(User.name).where(User.age == 30)
with_addr = select(User.name).join(Address)
session.execute(intersect(a30, with_addr)).scalars().all()   # ['Alice', 'Carol']
```

**Сортировка объединения**

```python
u = union(young, old).subquery()
select(u).order_by(u.c.name)
```

## Частые ошибки

- **Разное число или типы колонок в частях** — база откажется выполнять запрос. Все части обязаны совпадать по форме.
- **`union` там, где хватило бы `union_all`.** Удаление дубликатов стоит дорого: базе приходится сравнить весь результат.
- **`order_by` внутри частей обычно бессмысленен** — порядок задаётся для объединения целиком, для чего его оборачивают в подзапрос.
- **`except_` с подчёркиванием** — `except` это ключевое слово Python.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[subquery](subquery.md), [cte](cte.md), [select](select.md)
