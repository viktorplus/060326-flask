# .in_()

```python
select(User).where(User.username.in_(names))
```

**Что это.** Условие «значение входит в список»: SQL-оператор `IN`.

**Зачем.** Заменяет цепочку `or_(col == a, col == b, ...)` и позволяет одним запросом достать записи по списку идентификаторов.

## Сигнатура

```python
колонка.in_(iterable_or_subquery)
колонка.not_in(iterable)
```

## Минимальный пример

```python
names = ['username6132', 'username9452', 'username4585']
query = select(User).where(User.username.in_(names))
users = session.scalars(query).all()
```

## Типичные задачи

**Подзапрос вместо списка**

```python
subq = select(Address.user_id).where(Address.city == 'Berlin')
select(User).where(User.id.in_(subq))
```

**Отрицание**

```python
select(User).where(User.username.not_in(names))
```

## Частые ошибки

- **Подчёркивание в имени.** Метод называется `in_`, потому что `in` — зарезервированное слово Python. То же с `not_in`.
- **Пустой список.** `in_([])` даёт условие, которое никогда не истинно — запрос вернёт пусто. Это корректно, но легко принять за баг.
- **Очень длинный список.** У СУБД есть предел числа параметров; для тысяч значений используйте подзапрос или временную таблицу.

## Где в репозитории

- `l05_orm_relationships/app.py:240` — `query = select(User).where(User.username.in_(names))`

## См. также

[where](where.md), [or_](or_.md), [ilike](ilike.md)
