# session.add

```python
session.add(obj)      session.add_all([obj1, obj2])
```

**Что это.** Помечает объект как новый в сессии. SQL при этом НЕ выполняется.

**Зачем.** Сессия работает отложенно: сначала собирает все изменения, потом отправляет их одним разом. Это меньше обращений к базе и одна транзакция вместо десяти.

## Сигнатура

```python
session.add(instance)
session.add_all(instances)
```

## Минимальный пример

```python
with Session() as session:
    new_user = User(username='admin', age=20)
    session.add(new_user)        # SQL ещё НЕ ушёл в базу
    session.commit()             # вот теперь INSERT
```

## Типичные задачи

**Вставить пачку объектов**

```python
users = [User(username=f'user{i}', age=20 + i) for i in range(20)]
session.add_all(users)
session.commit()
```

**Вставить родителя вместе с детьми — user_id расставится сам**

```python
alice = User(name='Alice', age=30, addresses=[
    Address(city='New York'),
    Address(city='Los Angeles'),
])
session.add(alice)
session.commit()
```

## Частые ошибки

- **Забыть `commit()`.** Выход из блока `with` откатит транзакцию, и данных в базе не будет. Ошибки при этом никакой.
- **Ожидать, что `id` появится сразу после `add()`.** Он присваивается базой при вставке — то есть после `flush()` или `commit()`.
- **Добавлять объект, уже принадлежащий другой сессии** — `InvalidRequestError`.

## Где в репозитории

- `l04_orm_basics/app_1.py:82` — `session.add(new_user)`
- `l06_practice/app2.py:77` — `session.add(User(name='admin', age=20))`
- `l05_orm_relationships/app.py:128` *(строка-комментарий)* — `#     session.add(user)`
- `l05_orm_relationships/app.py:136` *(строка-комментарий)* — `#     session.add_all(users)`

## См. также

[session_commit](session_commit.md), [sessionmaker](sessionmaker.md), [IntegrityError](IntegrityError.md)
