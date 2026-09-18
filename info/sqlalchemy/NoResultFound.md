# NoResultFound

```python
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
```

**Что это.** Исключения, которыми `.one()` сообщает, что строк не нашлось или нашлось больше одной.

**Зачем.** Это не поломка, а сообщение о том, что данные не соответствуют ожиданию. Ловить их — нормальная часть работы с базой.

## Сигнатура

```python
try:
    obj = session.scalars(stmt).one()
except NoResultFound:
    ...
```

## Минимальный пример

```python
from sqlalchemy.exc import NoResultFound

try:
    user = session.scalars(select(User).where(User.id == 1)).one()
    print(user.username)
except NoResultFound:
    print('Пользователь с id=1 не найден')
```

## Типичные задачи

**Отдать 404 из Flask**

```python
try:
    user = session.scalars(stmt.where(User.id == user_id)).one()
except NoResultFound:
    abort(404, description='Пользователь не найден')
```

## Частые ошибки

- **Ловить общий `Exception`.** Тогда вместе с «не найдено» вы проглотите и настоящие ошибки подключения.
- **`MultipleResultsFound` там, где ждали одну запись,** означает проблему в данных — чаще всего не хватает уникального индекса.

## Где в репозитории

- `l05_orm_relationships/app.py:24` — `from sqlalchemy.exc import NoResultFound`
- `l05_orm_relationships/app.py:201` — `except NoResultFound:`
- `l05_orm_relationships/app.py:23` *(строка-комментарий)* — `# NoResultFound — исключение, которым .one() сообщает, что строк не нашлось.`
- `l05_orm_relationships/app.py:195` *(строка-комментарий)* — `# .one() требует ровно одну строку: 0 строк -> NoResultFound, 2+ -> MultipleResultsFound.`

## См. также

[first_one_all](first_one_all.md), [IntegrityError](IntegrityError.md), [session_get](session_get.md)
