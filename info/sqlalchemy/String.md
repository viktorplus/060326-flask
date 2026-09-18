# String

```python
from sqlalchemy import String, Integer, Text, Numeric, Boolean, DateTime
```

**Что это.** Типы колонок SQL. `String(n)` — это `VARCHAR(n)`, `Integer` — `INTEGER` и так далее.

**Зачем.** Аннотация `Mapped[str]` даёт тип по умолчанию, но длину и точность задают явно: `String(30)`, `Numeric(10, 2)`.

## Сигнатура

```python
String(length=None)   Integer   Text   Boolean
Numeric(precision, scale)   DateTime(timezone=False)   Date   Time   JSON
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `String(n)` | — | — | `VARCHAR(n)`. Для коротких строк с известным пределом |
| `Text` | — | — | Длинный текст без ограничения длины |
| `Integer / BigInteger` | — | — | Целые числа |
| `Numeric(p, s)` | — | — | Точное десятичное число. **Для денег брать его, а не Float** |
| `Float` | — | — | Число с плавающей точкой. Для денег не годится: `0.1 + 0.2 != 0.3` |
| `Boolean` | — | — | Логический тип |
| `DateTime(timezone=True)` | — | — | Дата и время. Часовой пояс поддерживают не все СУБД |
| `JSON` | — | — | Документ JSON в колонке |

## Минимальный пример

```python
from sqlalchemy import String, Integer, Numeric

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Numeric(10, 2))    # для денег
```

## Частые ошибки

- **`Float` для денег.** Двоичная дробь не представляет `0.1` точно, и суммы «уезжают» на копейки. Нужен `Numeric`, а в Python — `decimal.Decimal`.
- **`String` без длины.** SQLite стерпит, MySQL откажется создавать таблицу.
- **SQLite не проверяет длину `VARCHAR`.** Строка длиннее `String(30)` там сохранится целиком; на PostgreSQL тот же код упадёт. Проверяйте длину на уровне приложения — например Pydantic.

## Где в репозитории

- `l04_orm_basics/app_1.py:9` — `from sqlalchemy import create_engine, Column, String, Integer`
- `l04_orm_basics/app_1.py:53` — `username: Mapped[str] = mapped_column(String(30))`
- `l04_orm_basics/app_1.py:54` — `age: Mapped[int] = mapped_column(Integer)`
- `l04_orm_basics/app_2.py:5` — `from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData`

## См. также

[mapped_column](mapped_column.md), [Mapped](Mapped.md), [Column](Column.md)
