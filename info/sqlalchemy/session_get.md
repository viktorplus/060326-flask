# session.get

```python
user = session.get(User, 1)
```

**Что это.** Находит объект по первичному ключу. Возвращает объект или `None`.

**Зачем.** Самый частый и самый дешёвый вид выборки. Если объект уже загружен в этой сессии, запрос в базу вообще не пойдёт — он возьмётся из кэша сессии (identity map).

## Сигнатура

```python
session.get(entity, ident, options=None, with_for_update=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `entity` | type | — | Класс модели |
| `ident` | Any \\| tuple | — | Значение первичного ключа. Кортеж — для составного ключа |
| `options` | list | `None` | Настройки загрузки, например `joinedload(User.addresses)` |

## Минимальный пример

```python
user = session.get(User, 1)
if user:
    print(user.username)
else:
    print('не найден')

print(session.get(User, 100000))     # None — исключения НЕ будет
```

## Типичные задачи

**Обновить поле найденного объекта**

```python
user = session.get(User, 1)
if user:
    user.age = 35            # SQLAlchemy сам заметит изменение
    session.commit()         # UPDATE users SET age=35 WHERE id=1
```

## Частые ошибки

- **Забыть проверку на `None`.** Отсутствующий id вернёт `None`, и следующее же обращение к полю даст `AttributeError: 'NoneType' object has no attribute ...`.
- **Путать с `.one()`.** `get` возвращает `None`, а `.one()` бросает `NoResultFound`. Разное поведение при пустом результате.
- **Использовать для поиска не по ключу.** `get` работает ТОЛЬКО по первичному ключу; для остального нужен `select().where(...)`.

## Где в репозитории

- `l05_orm_relationships/app.py:206` — `user_one_get = session.get(User, 100000)`
- `l09_orm_practice/app.py:110` — `if session.get(User, deleted_id):`
- `l09_orm_practice/app.py:150` — `user_to_update = session.get(User, user_id_to_update)`
- `l05_orm_relationships/app.py:141` *(строка-комментарий)* — `#     user = session.get(User, 1)     # выборка по первичному ключу`

## См. также

[session_scalars](session_scalars.md), [first_one_all](first_one_all.md), [select](select.md)
