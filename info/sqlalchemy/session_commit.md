# session.commit

```python
session.commit()      session.rollback()      session.flush()
```

**Что это.** `commit()` отправляет накопленные изменения в базу и фиксирует транзакцию. `rollback()` откатывает. `flush()` отправляет SQL, но транзакцию не закрывает.

**Зачем.** Граница транзакции: до `commit()` изменения видны только внутри сессии, после — всем. Это же точка, где сработают ограничения базы.

## Сигнатура

```python
session.commit()
session.rollback()
session.flush()
```

## Минимальный пример

```python
with Session() as session:
    session.add(User(username='admin', age=20))
    session.commit()          # BEGIN ... INSERT ... COMMIT
```

## Типичные задачи

**Обработать нарушение уникальности**

```python
from sqlalchemy.exc import IntegrityError

try:
    session.add(User(id=6, username='admin', age=20))
    session.commit()
except IntegrityError:
    session.rollback()        # обязательно: без отката сессия непригодна
    print('Запись с таким id уже есть')
```

**Получить id до commit**

```python
session.add(user)
session.flush()               # INSERT ушёл, id присвоен
print(user.id)
session.commit()
```

## Частые ошибки

- **После исключения продолжать работать без `rollback()`.** Сессия остаётся в сломанном состоянии, и любой следующий запрос даёт `PendingRollbackError`.
- **Считать, что `flush()` фиксирует данные.** Он лишь отправляет SQL внутри текущей транзакции; без `commit()` всё откатится.
- **`commit()` в цикле по одной записи.** Каждая — отдельная транзакция, и это медленно. Собирайте пачку и делайте один `commit()`.

## Где в репозитории

- `l04_orm_basics/app_1.py:86` — `session.commit()`
- `l06_practice/app2.py:78` — `session.commit()`
- `l09_orm_practice/app.py:65` — `session.commit()`
- `l09_orm_practice/app.py:84` — `session.commit()`

## См. также

[session_add](session_add.md), [IntegrityError](IntegrityError.md), [sessionmaker](sessionmaker.md)
