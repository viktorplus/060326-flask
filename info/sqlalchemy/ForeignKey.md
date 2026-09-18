# ForeignKey

```python
from sqlalchemy import ForeignKey
```

**Что это.** Внешний ключ — связь на уровне базы данных: «в этой колонке лежит id из той таблицы».

**Зачем.** База сама следит за целостностью: нельзя сослаться на несуществующую запись. И именно по внешнему ключу `relationship` понимает, как соединять таблицы.

## Сигнатура

```python
mapped_column(ForeignKey('таблица.колонка', ondelete=None, onupdate=None))
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `column` | str \\| Column | — | `'users.id'` — имя ТАБЛИЦЫ и колонки, либо объект `User.id` |
| `ondelete` | str | `None` | Что делать при удалении родителя: `'CASCADE'`, `'SET NULL'`, `'RESTRICT'` |
| `onupdate` | str | `None` | То же при изменении ключа родителя |

## Минимальный пример

```python
class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True)
    # Строка 'users.id' — имя ТАБЛИЦЫ, а не класса
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # Эквивалент через объект (работает, если User объявлен выше):
    # user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
```

## Типичные задачи

**Удалять адреса вместе с пользователем силами базы**

```python
user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
```

**Необязательная связь**

```python
user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
```

## Частые ошибки

- **Написать имя КЛАССА вместо имени ТАБЛИЦЫ.** `ForeignKey('User.id')` — ошибка; нужно `ForeignKey('users.id')`, как в `__tablename__`.
- **SQLite по умолчанию не проверяет внешние ключи.** Нужно включать: `PRAGMA foreign_keys=ON`. Поэтому `ondelete='CASCADE'` там может тихо не работать.
- **Путать с `relationship`.** `ForeignKey` — колонка в базе; `relationship` — атрибут в Python. Это разные вещи, и обычно объявляют обе.

## Где в репозитории

- `l05_orm_relationships/app.py:11` — `from sqlalchemy import create_engine, Integer, String, ForeignKey`
- `l05_orm_relationships/app.py:72` — `user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))`
- `l07_orm_aggregates/app.py:4` — `from sqlalchemy import create_engine, Integer, String, ForeignKey`
- `l07_orm_aggregates/app.py:54` — `user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))`

## См. также

[relationship](relationship.md), [mapped_column](mapped_column.md), [join](join.md)
