# declarative_base

```python
from sqlalchemy.orm import declarative_base
```

**Что это.** Функция-фабрика базового класса в стиле SQLAlchemy 1.x. Делает то же, что `DeclarativeBase`.

**Зачем.** Встречается в старом коде и в учебных материалах. Знать полезно, писать новое — лучше на классе `DeclarativeBase`: он даёт подсказки типов в IDE.

## Сигнатура

```python
Base = declarative_base()
```

## Минимальный пример

```python
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()          # стиль 1.x

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
```

## Частые ошибки

- **Смешивать стили в одном проекте.** Работать будет (в `l06_practice/app2.py` как раз `declarative_base()` вместе с `Mapped`), но читателю приходится держать в голове два способа.
- **Ожидать подсказок типов.** `declarative_base()` возвращает динамически созданный класс, и статические анализаторы про его поля ничего не знают.

## Где в репозитории

- `l06_practice/app2.py:9` — `from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column`
- `l06_practice/app2.py:44` — `Base = declarative_base()`
- `l06_practice/app2.py:7` *(в закомментированном учебном блоке)* — `# declarative_base — фабрика базового класса в стиле 1.x`

## См. также

[DeclarativeBase](DeclarativeBase.md), [registry](registry.md)
