# .having()

```python
select(...).group_by(...).having(func.count(...) > 3)
```

**Что это.** Фильтрует УЖЕ СГРУППИРОВАННЫЕ строки по значению агрегата.

**Зачем.** `WHERE` применяется до группировки и про `count` ничего не знает. «Города, где больше трёх адресов» — это `HAVING`.

## Сигнатура

```python
select(...).group_by(...).having(*criteria)
```

## Минимальный пример

```python
from sqlalchemy import func, select

query = (select(Address.city, func.count(Address.id).label('addr_count'))
         .group_by(Address.city)
         .having(func.count(Address.id) > 3))

cities = session.execute(query).all()
```

## Типичные задачи

**WHERE и HAVING вместе: сначала отбор строк, потом отбор групп**

```python
query = (select(Address.city, func.count(Address.id).label('cnt'))
         .where(Address.city != 'Berlin')          # ДО группировки
         .group_by(Address.city)
         .having(func.count(Address.id) > 1))      # ПОСЛЕ группировки
```

## Частые ошибки

- **Путать с `where`.** `WHERE` — до группировки, по отдельным строкам; `HAVING` — после, по группам.
- **`having` без `group_by`.** Формально допустимо (вся выборка — одна группа), но почти всегда это ошибка.

## Где в репозитории

- `l08_orm_loading/app.py:120` *(в закомментированном учебном блоке)* — `#                    .label('addr_count')).group_by(Address.city).having(func.count(Address.id) > 3)`

## См. также

[group_by](group_by.md), [func](func.md), [where](where.md)
