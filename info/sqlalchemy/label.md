# .label()

```python
func.count(Address.id).label('addr_count')
```

**Что это.** Даёт имя вычисляемой колонке — это SQL-конструкция `AS`.

**Зачем.** Без имени к результату приходится обращаться по индексу `row[1]`. С именем — `row.addr_count`, и запрос читается сам.

## Сигнатура

```python
выражение.label('имя')
```

## Минимальный пример

```python
query = (select(Address.city, func.count(Address.id).label('addr_count'))
         .group_by(Address.city))

for row in session.execute(query):
    print(row.city, row.addr_count)      # вместо row[0], row[1]
```

## Типичные задачи

**Сортировка по имени вычисляемой колонки**

```python
from sqlalchemy import desc

query = (select(Address.city, func.count(Address.id).label('cnt'))
         .group_by(Address.city)
         .order_by(desc('cnt')))
```

## Частые ошибки

- **Имя метки совпало с именем колонки** — получится путаница в результате.
- **Обращаться к метке в `where`.** `WHERE` выполняется раньше, чем вычисляется `SELECT`, и метки там ещё не существует.

## Где в репозитории

- `l08_orm_loading/app.py:107` *(строка-комментарий)* — `#     # .label('addr_count') даёт колонке имя, по которому к ней можно обратиться как row.addr_count`
- `l08_orm_loading/app.py:108` *(строка-комментарий)* — `#     query = select(Address.city, func.count(Address.id).label('addr_count')).group_by(Address.city`
- `l08_orm_loading/app.py:120` *(строка-комментарий)* — `#                    .label('addr_count')).group_by(Address.city).having(func.count(Address.id) > 3)`

## См. также

[func](func.md), [group_by](group_by.md), [order_by](order_by.md)
