# .join()

```python
select(User).join(Address)
```

**Что это.** Соединяет таблицы в запросе. По умолчанию — `INNER JOIN`.

**Зачем.** Позволяет фильтровать и выбирать по полям связанной таблицы. Если есть `relationship` или `ForeignKey`, условие соединения SQLAlchemy выведет сам.

## Сигнатура

```python
select(...).join(target, onclause=None, *, isouter=False, full=False)
select(...).outerjoin(target)      # LEFT OUTER JOIN
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `target` | — | — | Модель или псевдоним, с которым соединяем |
| `onclause` | — | `None` | Условие соединения. Обычно выводится из `ForeignKey` |
| `isouter` | bool | `False` | `True` — `LEFT OUTER JOIN`: строки левой таблицы останутся даже без пары |

## Минимальный пример

```python
# Пользователи, у которых есть хотя бы один адрес
query = select(User).join(Address).distinct()

for user in session.scalars(query):
    print(user, user.addresses)
```

## Типичные задачи

**LEFT JOIN: оставить и тех, у кого связей нет**

```python
query = select(User).outerjoin(Address)       # Dave без адресов тоже попадёт
```

**Фильтр по полю связанной таблицы**

```python
query = select(User).join(Address).where(Address.city == 'Berlin')
```

**Соединение и загрузка связи одним запросом**

```python
from sqlalchemy.orm import contains_eager

query = (select(User)
         .join(Address)
         .options(contains_eager(User.addresses)))   # теперь join ЕЩЁ И наполняет коллекцию

# .unique() обязателен для коллекций: JOIN размножает строки родителя
for user in session.scalars(query).unique():
    print(user, user.addresses)
```

## Частые ошибки

- **Считать, что `join` загружает связь.** Самая частая путаница темы. `INNER JOIN` здесь работает как ФИЛЬТР «у кого есть хотя бы один адрес», а `user.addresses` он не наполняет — за это отвечает стратегия `lazy` или `contains_eager`.
- **Забыть `.distinct()`.** У пользователя два адреса — и он вернётся в выборке дважды.
- **`join` без `relationship` и без `ForeignKey`** — SQLAlchemy не знает, по каким колонкам соединять: `NoForeignKeysError`. Задайте `onclause` явно.
- **`contains_eager` по КОЛЛЕКЦИИ требует `.unique()` на результате.** Иначе `InvalidRequestError: The unique() method must be invoked on this Result`. Причина та же, что и с дублями: `JOIN` размножает строки родителя, и SQLAlchemy требует явно сказать, что их надо схлопнуть: `session.scalars(q).unique()`.

## Где в репозитории

- `l08_orm_loading/app.py:155` — `query = select(User).join(Address).distinct()`
- `l08_orm_loading/app.py:149` *(в закомментированном учебном блоке)* — `# .join(Address) — INNER JOIN: в выборку попадут только пользователи,`
- `l08_orm_loading/app.py:154` *(в закомментированном учебном блоке)* — `# Чтобы join ещё и загружал связь, нужен .options(contains_eager(User.addresses)).`

## См. также

[distinct](distinct.md), [lazy](lazy.md), [relationship](relationship.md), [aliased](aliased.md)
