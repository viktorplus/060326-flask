# update() / delete() — массовые

```python
from sqlalchemy import update, delete

session.execute(update(User).where(...).values(...))
```

**Что это.** Изменение и удаление строк ОДНИМ запросом, без загрузки объектов в память.

**Зачем.** Чтобы поднять возраст тысяче пользователей через ORM, пришлось бы загрузить тысячу объектов и получить тысячу `UPDATE`. Массовая форма делает это одним запросом.

## Сигнатура

```python
update(Model).where(условие).values(поле=значение)
delete(Model).where(условие)
result.rowcount      # сколько строк затронуто
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``.values(...)`` | — | — | Новые значения. Можно выражением: `values(age=User.age + 1)` |
| ``.where(...)`` | — | — | Какие строки менять. **Без него затронутся ВСЕ** |
| ``rowcount`` | int | — | Число затронутых строк |
| ``synchronize_session`` | str | `'auto'` | Как согласовать с объектами уже в сессии: `'auto'`, `'fetch'`, `'evaluate'`, `False` |

## Минимальный пример

```python
from sqlalchemy import delete, update

res = session.execute(update(User).where(User.age < 18).values(age=18))
print(res.rowcount)          # 1

res = session.execute(delete(Address).where(Address.city == 'Berlin'))
print(res.rowcount)          # 2

session.commit()
```

## Типичные задачи

**Изменение относительно текущего значения**

```python
session.execute(update(User).values(age=User.age + 1))    # всем +1 год
```

**Удалить и узнать, сколько удалилось**

```python
res = session.execute(delete(User).where(User.age < 18))
if res.rowcount == 0:
    print('под условие никто не попал')
session.commit()
```

## Частые ошибки

- **Забыть `where`.** `update(User).values(age=18)` изменит ВСЮ таблицу. Ошибка тихая: синтаксически всё верно.
- **Каскады и валидаторы ORM НЕ срабатывают.** `delete(User)` массовой формой не удалит связанные адреса, даже если в `relationship` прописан `cascade='all, delete-orphan'` — это работа ORM, а запрос идёт мимо неё. Останутся строки с несуществующим `user_id`. Нужен каскад — либо `session.delete()` по объекту, либо `ondelete='CASCADE'` на уровне базы.
- **Объекты, уже загруженные в сессию, могут устареть.** За это отвечает `synchronize_session`; значение по умолчанию справляется с большинством случаев, но после массовой операции безопаснее `session.expire_all()`.
- **Изменения не зафиксированы до `commit()`** — как и любые другие.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[session_delete](session_delete.md), [session_commit](session_commit.md), [where](where.md), [relationship](relationship.md)
