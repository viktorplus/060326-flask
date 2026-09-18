# aliased

```python
from sqlalchemy.orm import aliased
```

**Что это.** Псевдоним таблицы — SQL-конструкция `AS`. Позволяет сослаться на одну таблицу дважды в одном запросе.

**Зачем.** Самосоединение: «найти пользователей одного возраста», «сотрудник и его руководитель» — здесь таблица участвует в запросе два раза, и их надо различать.

## Сигнатура

```python
alias = aliased(Model, name=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `Model` | type | — | Класс модели |
| `name` | str | `None` | Имя псевдонима в SQL. Полезно при отладке лога |

## Минимальный пример

```python
from sqlalchemy.orm import aliased

user_alias = aliased(User, name='user_alias')

stmt = select(user_alias.username, func.count(user_alias.id)).group_by(user_alias.username)
result = session.execute(stmt).all()
```

## Типичные задачи

**Самосоединение: пары пользователей одного возраста**

```python
u1 = aliased(User, name='u1')
u2 = aliased(User, name='u2')

query = (select(u1.username, u2.username)
         .join(u2, u1.age == u2.age)
         .where(u1.id < u2.id))          # чтобы не было пар с самим собой и дублей
```

**Две связи на одну таблицу**

```python
manager = aliased(User, name='manager')
query = select(User.username, manager.username).join(manager, User.manager_id == manager.id)
```

## Частые ошибки

- **Считать, что псевдоним что-то меняет в простом запросе.** В `l07_orm_aggregates` результат с псевдонимом и без него одинаковый — это чистая демонстрация синтаксиса. Смысл появляется только при двух ссылках на одну таблицу.
- **Смешивать псевдоним и исходный класс в одном условии** — получится соединение таблицы с собой там, где вы этого не хотели.

## Где в репозитории

- `l07_orm_aggregates/app.py:12` — `from sqlalchemy.orm import aliased`
- `l07_orm_aggregates/app.py:86` — `user_aliase = aliased(User, name='user_aliase')`
- `l07_orm_aggregates/app.py:11` *(в закомментированном учебном блоке)* — `# aliased — псевдоним таблицы (SQL AS), нужен для самосоединений и читаемости запроса.`

## См. также

[join](join.md), [select](select.md), [func](func.md)
