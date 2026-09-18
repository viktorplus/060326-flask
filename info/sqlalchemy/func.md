# func

```python
from sqlalchemy import func
```

**Что это.** «Мост» к SQL-функциям: `func.count()`, `func.avg()`, `func.min()`, `func.max()`, `func.sum()`, `func.lower()`, `func.now()`.

**Зачем.** Считать среднее в Python — значит вытащить всю таблицу. `func.avg` считает это на стороне базы и возвращает одно число.

## Сигнатура

```python
func.<любое_имя_функции_СУБД>(аргументы)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `func.count(col)` | — | — | Количество строк. `func.count()` — всех, `func.count(col)` — где колонка не NULL |
| `func.avg(col)` | — | — | Среднее |
| `func.min / max / sum` | — | — | Минимум, максимум, сумма |
| `func.lower / upper` | — | — | Регистр строки |
| `func.now()` | — | — | Текущее время на сервере БД |
| `func.coalesce(a, b)` | — | — | Первое не-NULL значение |

## Минимальный пример

```python
from sqlalchemy import func, select

avg_age = session.scalar(select(func.avg(User.age)))
print(avg_age)

query = select(func.count(User.id), func.min(User.age), func.max(User.age))
count, min_age, max_age = session.execute(query).one()
```

## Типичные задачи

**Количество с группировкой**

```python
query = select(User.username, func.count(User.id)).group_by(User.username)
rows = session.execute(query).all()
```

**Регистронезависимое сравнение**

```python
select(User).where(func.lower(User.username) == name.lower())
```

## Частые ошибки

- **`func.avg` на пустой таблице возвращает `None`, а не 0.** Арифметика с результатом без проверки даст `TypeError`.
- **`scalars` вместо `execute` для нескольких агрегатов** — вернётся только первый, молча.
- **`func.count(col)` не считает `NULL`.** Если нужно число строк, берите `func.count()`.
- **`func` не проверяет имя функции.** `func.чепуха()` соберётся и упадёт уже в базе — имя подставляется в SQL как есть.

## Где в репозитории

- `l07_orm_aggregates/app.py:68` — `query = select(func.avg(User.age))`
- `l07_orm_aggregates/app.py:76` — `query = select(User.username, func.count(User.id)).group_by(User.username)`
- `l07_orm_aggregates/app.py:90` — `stmt = select(user_aliase.username, func.count(user_aliase.id)).group_by(user_aliase.username)`
- `l07_orm_aggregates/app.py:8` *(строка-комментарий)* — `# func — «мост» к SQL-функциям: func.avg(...), func.count(...), func.max(...).`

## См. также

[group_by](group_by.md), [session_scalar](session_scalar.md), [having](having.md)
