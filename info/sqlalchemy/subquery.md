# subquery

```python
subq = select(...).subquery()
select(...).join(subq, User.id == subq.c.user_id)
```

**Что это.** Превращает запрос в подзапрос, к которому можно присоединиться как к таблице. Колонки доступны через `.c.<имя>`.

**Зачем.** Когда нужно сначала что-то сгруппировать, а потом соединить результат с основной таблицей. В отличие от `scalar_subquery`, возвращает не одно значение, а набор строк.

## Сигнатура

```python
subq = select(колонки).subquery(name=None)
subq.c.<имя колонки>
aliased(Model, subq)          # отобразить модель на подзапрос
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``.subquery()`` | — | — | Делает из `Select` объект, пригодный для `join` и `FROM` |
| ``.c`` | — | — | Доступ к колонкам подзапроса. Имя берётся из `label()` или из исходной колонки |
| ``name`` | str | авто | Имя в SQL. Полезно при чтении лога |
| ``aliased(Model, subq)`` | — | — | Позволяет работать с подзапросом как с моделью, а не с кортежами |

## Минимальный пример

```python
from sqlalchemy import func, select

# Сколько адресов у каждого пользователя
counts = (select(Address.user_id, func.count(Address.id).label('n'))
          .group_by(Address.user_id)
          .subquery())

# Присоединяем результат к пользователям
rows = session.execute(
    select(User.name, counts.c.n)
    .join(counts, User.id == counts.c.user_id)
    .order_by(counts.c.n.desc())
).all()
```

Вывод:

```
[('Alice', 2), ('Frank', 2), ('Bob', 1), ('Carol', 1), ('Eve', 1)]
```

## Типичные задачи

**Получить объекты модели, а не кортежи**

```python
from sqlalchemy.orm import aliased

subq = select(User).where(User.age > 25).subquery()
adults = aliased(User, subq)
session.scalars(select(adults)).all()     # это объекты User
```

**Соединить с агрегатом и отфильтровать по нему**

```python
counts = (select(Address.user_id, func.count(Address.id).label('n'))
          .group_by(Address.user_id).subquery())

select(User).join(counts, User.id == counts.c.user_id).where(counts.c.n > 1)
```

## Частые ошибки

- **Обращаться к колонкам напрямую, без `.c`.** У подзапроса свои колонки: `subq.n` не сработает, нужно `subq.c.n`.
- **Колонка без `label()` получает имя исходной.** `func.count(Address.id)` без метки окажется под неудобным автоматическим именем — давайте метки.
- **Путать с `scalar_subquery()`.** Тот возвращает ОДНО значение и подставляется в условие; этот — набор строк и подставляется в `FROM`/`JOIN`.
- **`session.scalars(select(subq))` вернёт кортежи, а не модели.** Чтобы получить объекты, нужен `aliased(Model, subq)`.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[scalar_subquery](scalar_subquery.md), [join](join.md), [cte](cte.md), [group_by](group_by.md)
