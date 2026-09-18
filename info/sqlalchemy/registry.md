# registry

```python
from sqlalchemy.orm import registry
```

**Что это.** Реестр соответствий «класс — таблица». Позволяет связать обычный класс с таблицей вручную, без наследования от `Base`.

**Зачем.** Когда класс уже существует и менять его нельзя (чужая библиотека, доменная модель, которую не хочется привязывать к ORM).

## Сигнатура

```python
mapper_registry = registry()
mapper_registry.map_imperatively(Class, table)
```

## Минимальный пример

```python
from sqlalchemy.orm import registry

mapper_registry = registry()

user_table = Table('users', mapper_registry.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('username', String(30)),
                   Column('age', Integer))

class User:
    def __init__(self, username, age):
        self.username = username
        self.age = age

mapper_registry.map_imperatively(User, user_table)
```

## Частые ошибки

- **Дважды связать один класс** — `ArgumentError`. Класс может быть сопоставлен только одной таблице.
- **Смешивать `registry()` и `DeclarativeBase` в одном проекте** без необходимости. Выберите один стиль.

## Где в репозитории

- `l04_orm_basics/app_2.py:18` *(строка-комментарий)* — `# mapped_register = registry()`

## См. также

[Table](Table.md), [DeclarativeBase](DeclarativeBase.md), [automap_base](automap_base.md)
