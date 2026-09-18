# first / one / one_or_none / all

```python
res.first()   res.one()   res.one_or_none()   res.all()
```

**Что это.** Четыре способа забрать результат. Отличаются тем, что происходит при нуле строк и при нескольких.

**Зачем.** Выбор метода — это заявление о том, чего вы ждёте от данных. Правильно выбранный метод ловит ошибку в данных сразу, а не через сто строк.

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``.first()`` | — | — | 0 строк → `None`; 1+ → первая. **Требует проверки на `None`** |
| ``.one()`` | — | — | 0 → `NoResultFound`; 2+ → `MultipleResultsFound`; ровно 1 → объект |
| ``.one_or_none()`` | — | — | 0 → `None`; 2+ → исключение; 1 → объект. Компромисс |
| ``.all()`` | — | — | Всегда список. 0 строк → пустой список, исключений нет |

## Минимальный пример

```python
stmt = select(User)

# ЧАСТАЯ ОШИБКА: на наполненной базе работает, на пустой падает
# user = session.scalars(stmt).first()
# print(user.id)          # AttributeError: 'NoneType' object has no attribute 'id'

# Правильно:
user = session.scalars(stmt).first()
if user:
    print(user.id, user.username)
else:
    print('Таблица пуста')
```

## Типичные задачи

**.one() требует try/except — на None он не проверяется**

```python
from sqlalchemy.exc import NoResultFound

try:
    user = session.scalars(stmt.where(User.id == 1)).one()
    print(user.username)
except NoResultFound:
    print('Пользователь с id=1 не найден')
```

**one_or_none: ноль допустим, два — это ошибка данных**

```python
user = session.scalars(stmt.where(User.email == email)).one_or_none()
if user:
    print(user.username)
# два пользователя с одной почтой -> MultipleResultsFound, и это правильно
```

## Частые ошибки

- **Обратиться к полю сразу после `.first()`.** Классика: скрипт работает, пока база наполнена, и падает на пустой. Так было в `l05_orm_relationships`.
- **Проверять результат `.one()` на `None`.** Он никогда не возвращает `None` — он бросает исключение. Нужен `try/except NoResultFound`.
- **`.all()` на огромной таблице.** Весь результат окажется в памяти. Для больших выборок обходите результат итератором или добавьте `.limit()`.

## Где в репозитории

- `l05_orm_relationships/app.py:187` — `user_first = session.scalars(stmt).first()`
- `l05_orm_relationships/app.py:199` — `user_one = session.scalars(stmt.where(User.id == 1)).one()`
- `l05_orm_relationships/app.py:210` — `user_one = session.scalars(stmt.where(User.id == 1)).one_or_none()`
- `l05_orm_relationships/app.py:218` — `users_adult = session.scalars(query).all()`

## См. также

[session_scalars](session_scalars.md), [NoResultFound](NoResultFound.md), [session_get](session_get.md)
