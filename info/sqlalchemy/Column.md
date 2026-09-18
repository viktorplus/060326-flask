# Column

```python
from sqlalchemy import Column
```

**Что это.** Описание колонки в стиле SQLAlchemy 1.x: `Column(Integer, primary_key=True)`.

**Зачем.** Встречается в старом коде и нужен при императивном описании таблиц через `Table`. В новых моделях его заменяет `mapped_column`.

## Сигнатура

```python
Column(name, type_, *args, primary_key=False, nullable=True, default=None, index=False)
```

## Минимальный пример

```python
# Стиль 1.x
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30))

# Тот же результат в стиле 2.0 — но с подсказками типов
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
```

## Частые ошибки

- **Ожидать подсказок типов.** IDE не знает, что `user.id` это `int` — в этом главное отличие от `mapped_column`.
- **`nullable` по умолчанию разное.** У `Column` — `True`, а у `Mapped[int]` — `False`. При переписывании кода со старого стиля на новый это меняет схему.

## Где в репозитории

- `l04_orm_basics/app_1.py:45` *(строка-комментарий)* — `# id = Column(Integer, primary_key=True)`
- `l04_orm_basics/app_1.py:46` *(строка-комментарий)* — `# name = Column(String)`
- `l04_orm_basics/app_1.py:47` *(строка-комментарий)* — `# email = Column(String)`
- `l04_orm_basics/app_2.py:21` *(строка-комментарий)* — `#                    Column('id', Integer, primary_key=True),`

## См. также

[mapped_column](mapped_column.md), [Table](Table.md), [String](String.md)
