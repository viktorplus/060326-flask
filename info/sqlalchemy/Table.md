# Table

```python
from sqlalchemy import Table, Column, MetaData
```

**Что это.** Описание таблицы объектом, без класса модели. Основа императивного подхода (SQLAlchemy Core).

**Зачем.** Нужен в двух случаях: промежуточная таблица для связи «многие ко многим» (класс для неё избыточен) и работа с базой вообще без ORM.

## Сигнатура

```python
Table(name, metadata, *columns, schema=None, extend_existing=False)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `name` | str | — | Имя таблицы в базе |
| `metadata` | MetaData | — | Реестр, куда таблица регистрируется |
| `*columns` | Column | — | Колонки |

## Минимальный пример

```python
from sqlalchemy import Table, Column, ForeignKey

tags_association = Table(
    'tags_association', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('tag_id', ForeignKey('tags.id')),
)
```

## Типичные задачи

**Императивный маппинг: таблица и класс связываются отдельно**

```python
from sqlalchemy.orm import registry

mapper_registry = registry()

user_table = Table('users', mapper_registry.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('username', String(30)))

class User:                       # обычный класс, без наследования от Base
    def __init__(self, username):
        self.username = username

mapper_registry.map_imperatively(User, user_table)
```

## Частые ошибки

- **Забыть передать `metadata`.** Таблица не попадёт в реестр, и `create_all` её не создаст.
- **Объявить промежуточную таблицу как модель.** Для связи «многие ко многим» без дополнительных полей класс не нужен — достаточно `Table`.

## Где в репозитории

- `l04_orm_basics/app_2.py:20` *(в закомментированном учебном блоке)* — `# user_table = Table('users', mapped_register.metadata,`
- `l04_orm_basics/app_2.py:63` *(в закомментированном учебном блоке)* — `# metadata = MetaData()`
- `l05_orm_relationships/app.py:94` *(в закомментированном учебном блоке)* — `# tags_association = Table(`

## См. также

[Column](Column.md), [registry](registry.md), [relationship](relationship.md)
