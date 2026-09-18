# over — оконные функции

```python
func.row_number().over(partition_by=..., order_by=...)
```

**Что это.** Оконная функция: считает агрегат, **не схлопывая строки**. В SQL — `... OVER (PARTITION BY ... ORDER BY ...)`.

**Зачем.** `GROUP BY` превращает группу в одну строку. Окно оставляет все строки на месте и дописывает к каждой вычисленное значение: ранг внутри города, долю от общего, предыдущее значение. Без окон такие задачи требуют самосоединения или двух запросов.

## Сигнатура

```python
func.<функция>().over(partition_by=None, order_by=None, rows=None, range_=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``partition_by`` | колонка \\| список | `None` | Как делить строки на окна. Аналог `GROUP BY`, но строки не схлопываются |
| ``order_by`` | — | `None` | Порядок ВНУТРИ окна. Нужен для `row_number`, `rank`, `lag`, `lead` |
| ``rows` / `range_`` | кортеж | `None` | Границы окна: `(None, 0)` — от начала до текущей строки |
| ``func.row_number()`` | — | — | Порядковый номер в окне: 1, 2, 3 без пропусков |
| ``func.rank()`` | — | — | Ранг с пропусками при равенстве: 1, 1, 3 |
| ``func.dense_rank()`` | — | — | Ранг без пропусков: 1, 1, 2 |
| ``func.lag()` / `func.lead()`` | — | — | Значение предыдущей / следующей строки окна |

## Минимальный пример

```python
from sqlalchemy import func, select

# Ранг пользователя по возрасту ВНУТРИ каждого города
rank = func.row_number().over(partition_by=Address.city, order_by=User.age.desc())

rows = session.execute(
    select(Address.city, User.name, User.age, rank.label('rank'))
    .join(User)
    .order_by(Address.city, 'rank')
).all()
```

Вывод:

```
('Berlin', 'Frank', 45, 1)   ('Berlin', 'Eve', 27, 2)
('LA', 'Alice', 30, 1)       ('LA', 'Carol', 30, 2)
('NY', 'Frank', 45, 1)       ('NY', 'Alice', 30, 2)   ('NY', 'Bob', 22, 3)
```

## Типичные задачи

**Общее количество рядом с каждой строкой**

```python
total = func.count().over()          # окно без partition_by — вся выборка
select(User.name, total.label('total'))
# [('Alice', 6), ('Bob', 6), ...] — в каждой строке общее число
```

**Доля от суммы по группе**

```python
share = Address.id / func.count(Address.id).over(partition_by=Address.city)
```

**Взять по одному представителю от каждой группы**

```python
# «Самый старший в каждом городе»: нумеруем и берём первых
rn = func.row_number().over(partition_by=Address.city, order_by=User.age.desc())
sub = select(User.name, Address.city, rn.label('rn')).join(User).subquery()
select(sub.c.name, sub.c.city).where(sub.c.rn == 1)
```

## Частые ошибки

- **Фильтровать по окну в `WHERE`.** Оконные функции вычисляются ПОСЛЕ `WHERE`, поэтому `where(rank == 1)` не соберётся. Нужен подзапрос — как в примере выше.
- **`row_number` без `order_by`** даёт непредсказуемую нумерацию.
- **Путать `rank` и `dense_rank`.** При равных значениях `rank` пропускает номера (1, 1, 3), `dense_rank` — нет (1, 1, 2).
- **Окно без `partition_by` охватывает всю выборку** — это законно и часто именно то, что нужно, но легко получить случайно.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[func](func.md), [group_by](group_by.md), [subquery](subquery.md), [order_by](order_by.md)
