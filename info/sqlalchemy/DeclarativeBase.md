# DeclarativeBase

```python
from sqlalchemy.orm import DeclarativeBase
```

**Что это.** Базовый класс для моделей в стиле SQLAlchemy 2.0. Наследники становятся таблицами.

**Зачем.** Он держит `metadata` — реестр всех описанных таблиц. Именно по нему `create_all` понимает, что нужно создать в базе.

## Сигнатура

```python
class Base(DeclarativeBase):
    pass
```

## Минимальный пример

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
```

## Типичные задачи

**Общие поля для всех моделей**

```python
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
```

**Свои соответствия типов Python и SQL**

```python
from sqlalchemy import String

class Base(DeclarativeBase):
    type_annotation_map = {str: String(100)}   # str по умолчанию -> VARCHAR(100)
```

## Частые ошибки

- **Забыть `__tablename__`.** `ArgumentError: Class does not have a __table__ or __tablename__`.
- **Две модели с одинаковым `__tablename__` в одной `metadata`** — `InvalidRequestError`. В этом курсе каждый урок объявляет свои `User`/`Address` заново, но в разных файлах и с разными `Base`, поэтому конфликта нет.
- **Использовать `Base` из другого урока.** У каждого файла своя `metadata`; смешивать их нельзя.

## Где в репозитории

- `l04_orm_basics/app_1.py:14` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column`
- `l04_orm_basics/app_1.py:34` — `class Base(DeclarativeBase):`
- `l04_orm_basics/app_2.py:8` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry, Mapped, mapped_column`
- `l04_orm_basics/app_2.py:79` — `class Base(DeclarativeBase):`

## См. также

[declarative_base](declarative_base.md), [mapped_column](mapped_column.md), [create_all](create_all.md)
