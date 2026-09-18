# or_ / and_ / not_

```python
from sqlalchemy import or_, and_, not_
```

**Что это.** Логические операторы для условий SQL. Заменяют питоновские `or`, `and`, `not`, которые здесь работать не могут.

**Зачем.** Питоновские `and`/`or`/`not` требуют привести операнд к `bool`, а условие SQL — это описание выражения, а не истина или ложь. SQLAlchemy на такую попытку бросает `TypeError`, поэтому составное условие собирают функциями.

## Сигнатура

```python
or_(*clauses)    and_(*clauses)    not_(clause)
```

## Минимальный пример

```python
from sqlalchemy import or_, not_

# ИЛИ
query = select(User).where(or_(User.username.ilike('U%'), User.username.ilike('A%')))
query = select(User).where(or_(User.age < 20, User.age > 50))

# НЕ
query = select(User).where(not_(User.age > 40))      # NOT (age > 40)

# И: отдельная функция обычно не нужна — два .where() уже дают AND
query = select(User).where(User.age > 40).where(User.age < 50)
```

## Типичные задачи

**Сложное условие со скобками**

```python
from sqlalchemy import and_, or_

query = select(User).where(
    or_(
        and_(User.age >= 18, User.age <= 25),
        User.username.ilike('admin%'),
    )
)
```

**Собрать список условий динамически**

```python
conditions = []
if min_age:
    conditions.append(User.age >= min_age)
if name:
    conditions.append(User.username.ilike(f'{name}%'))

query = select(User)
if conditions:
    query = query.where(and_(*conditions))
```

## Частые ошибки

- **Питоновские `and` / `or` / `not`.** `User.age > 20 and User.age < 50` даёт `TypeError: Boolean value of this clause is not defined`. Причина: `and` спрашивает у первого операнда его истинность, а условие SQL истинностью не обладает — оно описывает выражение. SQLAlchemy 2.0 специально запрещает такое приведение, чтобы ошибка не превратилась в молча неверный фильтр.
- **Забыть скобки в смешанном условии.** `or_` и `and_` имеют разный приоритет в SQL — вкладывайте их явно.
- **`not_` вместо `!=`.** Для простого неравенства достаточно `User.age != 30`.

## Где в репозитории

- `l05_orm_relationships/app.py:246` — `query = select(User).where(or_(User.username.ilike('U%'), User.username.ilike('A%')))`
- `l05_orm_relationships/app.py:251` — `query = select(User).where(or_(User.age < 20, User.age > 50))`
- `l05_orm_relationships/app.py:256` — `query = select(User).where(not_(User.age > 40))`
- `l05_orm_relationships/app.py:244` *(строка-комментарий)* — `# or_(...) объединяет условия через OR. Питоновский or здесь использовать НЕЛЬЗЯ —`

## См. также

[where](where.md), [in_](in_.md), [having](having.md)
