# cte

```python
c = select(...).cte('имя')
select(c.c.колонка).where(...)
```

**Что это.** Обобщённое табличное выражение — SQL `WITH имя AS (...)`. По смыслу как подзапрос, но с именем и возможностью рекурсии.

**Зачем.** Читается лучше вложенного подзапроса: сначала объявили промежуточный набор, потом им пользуетесь. А рекурсивный CTE — единственный способ обойти дерево (категории, подчинённые, комментарии) одним запросом.

## Сигнатура

```python
c = select(колонки).cte(name=None, recursive=False)
c.c.<колонка>
base.union_all(шаг)          # тело рекурсии
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``name`` | str | авто | Имя выражения в SQL |
| ``recursive`` | bool | `False` | Разрешить ссылаться на само выражение внутри него |
| ``.c`` | — | — | Доступ к колонкам, как у подзапроса |

## Минимальный пример

```python
from sqlalchemy import func, select

by_city = (select(Address.city, func.count(Address.id).label('n'))
           .group_by(Address.city)
           .cte('by_city'))

rows = session.execute(select(by_city.c.city, by_city.c.n).where(by_city.c.n > 1)).all()
```

Вывод:

```
[('Berlin', 2), ('LA', 2), ('NY', 3)]
```

## Типичные задачи

**Рекурсивный CTE: последовательность чисел**

```python
from sqlalchemy import literal

base = select(literal(1).label('n')).cte('seq', recursive=True)
seq = base.union_all(select(base.c.n + 1).where(base.c.n < 5))

session.execute(select(seq.c.n)).scalars().all()      # [1, 2, 3, 4, 5]
```

**Рекурсивный обход дерева категорий**

```python
# Первый шаг — корень; дальше присоединяем детей к уже найденным
base = select(Category.id, Category.parent_id, Category.name).where(
    Category.parent_id.is_(None)).cte('tree', recursive=True)

tree = base.union_all(
    select(Category.id, Category.parent_id, Category.name)
    .join(base, Category.parent_id == base.c.id)
)
session.execute(select(tree)).all()
```

**Несколько CTE подряд**

```python
a = select(...).cte('a')
b = select(a.c.x).where(...).cte('b')      # b использует a
select(b)
```

## Частые ошибки

- **Рекурсия без условия остановки** зациклит запрос. В теле обязательно должно быть условие, которое рано или поздно перестанет давать новые строки.
- **`union` вместо `union_all` в рекурсии** молча убирает дубликаты и может изменить результат обхода. Обычно нужен `union_all`.
- **SQLite поддерживает CTE с версии 3.8.3** — в современных сборках Python это есть, но на старой СУБД конструкция просто не соберётся.
- **CTE — не всегда оптимизация.** В некоторых СУБД он материализуется целиком, и обычный подзапрос оказывается быстрее.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[subquery](subquery.md), [union](union.md), [join](join.md)
