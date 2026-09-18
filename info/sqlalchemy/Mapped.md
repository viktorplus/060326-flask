# Mapped

```python
from sqlalchemy.orm import Mapped
```

**Что это.** Аннотация типа для колонки: `Mapped[int]`, `Mapped[str]`, `Mapped[list['Address']]`.

**Зачем.** Из неё SQLAlchemy выводит тип колонки и то, обязательна ли она. Заодно IDE и mypy начинают понимать, что `user.age` — это `int`, а не «что-то».

## Сигнатура

```python
имя: Mapped[тип] = mapped_column(...)
имя: Mapped[тип]                      # без вызова, если параметры не нужны
имя: Mapped[тип | None]               # NULL разрешён
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `Mapped[int]` | — | — | `NOT NULL` по умолчанию |
| `Mapped[int \\| None]` | — | — | `NULL` разрешён |
| `Mapped[list['Other']]` | — | — | Связь «один ко многим» через `relationship` |
| `Mapped['Other']` | — | — | Связь «многие к одному» или «один к одному» |

## Минимальный пример

```python
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]                                  # вызов не нужен: тип ясен из аннотации
    nickname: Mapped[str | None]                      # NULL разрешён
    addresses: Mapped[list['Address']] = relationship(back_populates='user')
```

## Частые ошибки

- **Считать, что `Mapped[int]` разрешает `NULL`.** Наоборот: без `| None` колонка получит `NOT NULL`. Это отличие от привычного «по умолчанию всё необязательно».
- **Имя связанного класса без кавычек, когда он объявлен ниже.** `Mapped[list[Address]]` до объявления `Address` даст `NameError`. Строка `'Address'` решает проблему.

## Где в репозитории

- `l04_orm_basics/app_1.py:14` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column`
- `l04_orm_basics/app_1.py:51` — `id: Mapped[int] = mapped_column(primary_key=True)`
- `l04_orm_basics/app_1.py:53` — `username: Mapped[str] = mapped_column(String(30))`
- `l04_orm_basics/app_1.py:54` — `age: Mapped[int] = mapped_column(Integer)`

## См. также

[mapped_column](mapped_column.md), [relationship](relationship.md), [DeclarativeBase](DeclarativeBase.md)
