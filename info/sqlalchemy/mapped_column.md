# mapped_column

```python
from sqlalchemy.orm import mapped_column
```

**Что это.** Описывает параметры колонки: первичный ключ, длину, внешний ключ, значение по умолчанию.

**Зачем.** Тип берётся из `Mapped[...]`, а всё остальное — отсюда. Современная замена старому `Column(Integer, primary_key=True)`.

## Сигнатура

```python
mapped_column(__type=None, *, primary_key=False, nullable=None, default=None,
              server_default=None, unique=False, index=False, autoincrement='auto',
              ForeignKey(...), comment=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `__type` | TypeEngine | из `Mapped` | Тип SQL: `String(30)`, `Integer`, `Numeric(10, 2)` |
| `primary_key` | bool | `False` | Первичный ключ. Для целого в SQLite автоматически автоинкрементный |
| `nullable` | bool \\| None | из `Mapped` | Разрешить `NULL`. Обычно задаётся через `Mapped[T \| None]` |
| `default` | Any | `None` | Значение по умолчанию на стороне Python |
| `server_default` | str | `None` | Значение по умолчанию на стороне БД: `text('now()')` |
| `unique` | bool | `False` | Уникальный индекс |
| `index` | bool | `False` | Обычный индекс |
| `autoincrement` | str \\| bool | `'auto'` | Автоинкремент для целочисленного первичного ключа |

## Минимальный пример

```python
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)
```

## Типичные задачи

**Уникальное поле с индексом**

```python
email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
```

**Внешний ключ**

```python
user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
```

**Время создания записи**

```python
from datetime import datetime
created_at: Mapped[datetime] = mapped_column(default=datetime.now)
```

## Частые ошибки

- **Задавать `id` вручную при вставке.** `User(id=6, ...)` отработает один раз, а на втором запуске даст `IntegrityError: UNIQUE constraint failed: users.id`. Коварство в том, что «первый раз получилось». Не указывайте `id` — база подставит сама. Разбор — в [l04_orm_basics](../../l04_orm_basics/SCHEMA.md).
- **`String` без длины в MySQL.** SQLite это стерпит, MySQL потребует `VARCHAR(n)`. Пишите `String(30)` сразу — переносимее.
- **`default` против `server_default`.** Первое вычисляет Python при вставке из ORM; второе живёт в схеме таблицы и сработает даже при вставке в обход ORM.

## Где в репозитории

- `l04_orm_basics/app_1.py:14` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column`
- `l04_orm_basics/app_1.py:51` — `id: Mapped[int] = mapped_column(primary_key=True)`
- `l04_orm_basics/app_1.py:53` — `username: Mapped[str] = mapped_column(String(30))`
- `l04_orm_basics/app_1.py:54` — `age: Mapped[int] = mapped_column(Integer)`

## См. также

[Mapped](Mapped.md), [ForeignKey](ForeignKey.md), [String](String.md)
