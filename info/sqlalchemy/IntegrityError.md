# IntegrityError

```python
from sqlalchemy.exc import IntegrityError
```

**Что это.** Исключение при нарушении ограничения базы: уникальность, внешний ключ, `NOT NULL`.

**Зачем.** База — последний рубеж проверки данных. Даже если приложение что-то пропустило, ограничение сработает здесь.

## Сигнатура

```python
try:
    session.commit()
except IntegrityError:
    session.rollback()
```

## Минимальный пример

```python
from sqlalchemy.exc import IntegrityError

try:
    session.add(User(id=6, username='admin', age=20))
    session.commit()
except IntegrityError as e:
    session.rollback()             # ОБЯЗАТЕЛЬНО
    print('UNIQUE constraint failed: users.id')
```

## Типичные задачи

**Вернуть клиенту 409 Conflict вместо 500**

```python
try:
    session.commit()
except IntegrityError:
    session.rollback()
    return jsonify(error='Такая запись уже существует'), 409
```

## Частые ошибки

- **Задавать первичный ключ вручную.** `User(id=6, ...)` отработает один раз, а на втором запуске даст `IntegrityError`. Именно эта ошибка была в `l04_orm_basics/app_1.py`.
- **Не сделать `rollback()`.** Сессия остаётся в сломанном состоянии; следующий запрос даст `PendingRollbackError`.
- **Исключение возникает на `commit()`, а не на `add()`.** SQL уходит в базу отложенно, поэтому `try` нужно оборачивать вокруг `commit()`.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[session_commit](session_commit.md), [mapped_column](mapped_column.md), [NoResultFound](NoResultFound.md)
