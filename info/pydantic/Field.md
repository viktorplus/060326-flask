# Field

```python
from pydantic import Field
```

**Что это.** Описывает ограничения и метаданные одного поля: границы чисел, длину строк, значение по умолчанию, описание для документации.

**Зачем.** Тип отвечает только за «это число», а `Field` — за «это число от 18 до 70». Ограничения в объявлении поля заменяют россыпь `if` внутри валидаторов.

## Сигнатура

```python
Field(default=PydanticUndefined, *, default_factory=None, alias=None,
      title=None, description=None, gt=None, ge=None, lt=None, le=None,
      min_length=None, max_length=None, pattern=None, frozen=None, exclude=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `default` | Any | обязательное | Значение по умолчанию. `...` (Ellipsis) — поле обязательное |
| `default_factory` | Callable | `None` | Функция, которая вызывается для КАЖДОГО объекта. Для `uuid4`, `list`, `datetime.now` |
| `gt / ge` | int \\| float | `None` | Больше / больше либо равно |
| `lt / le` | int \\| float | `None` | Меньше / меньше либо равно |
| `min_length / max_length` | int | `None` | Длина строки, списка, словаря |
| `pattern` | str | `None` | Регулярное выражение для строки |
| `alias` | str | `None` | Другое имя поля во входных данных: `Field(alias='firstName')` |
| `description` | str | `None` | Пояснение. Попадает в схему JSON и в документацию API |
| `frozen` | bool | `None` | Запретить изменение поля после создания объекта |
| `exclude` | bool | `None` | Не включать поле в результат `model_dump()` |

## Минимальный пример

```python
from typing import Annotated
from pydantic import BaseModel, Field

class User(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50, description='Имя пользователя')]
    age: Annotated[int, Field(ge=18, le=70)]
    salary: float = Field(gt=0, description='Больше нуля')
```

## Типичные задачи

**Обязательное поле с описанием — Ellipsis первым аргументом**

```python
password: str = Field(..., min_length=8, description='Не менее 8 символов')
```

**Генерируемое значение: default_factory вместо default**

```python
from uuid import UUID, uuid4

id: UUID = Field(default_factory=uuid4)    # вызовется для каждого объекта
# id: UUID = uuid4()   <- ТАК НЕЛЬЗЯ: вычислится один раз при объявлении класса,
#                          и у всех объектов будет ОДИН id
```

**Переиспользуемый тип с ограничением**

```python
from typing import Annotated

positive_number = Annotated[float, Field(gt=0)]

class Product(BaseModel):
    price: positive_number       # правило описано один раз

class Order(BaseModel):
    total: positive_number
```

## Частые ошибки

- **`default` вместо `default_factory` для изменяемых и генерируемых значений.** `id: UUID = uuid4()` вычислится ОДИН раз при загрузке модуля — все объекты получат одинаковый id. Нужен `Field(default_factory=uuid4)`.
- **Ограничение поля конфликтует с настройкой модели.** `str_to_upper=True` в `model_config` и валидатор, требующий `value.istitle()`, несовместимы: `'JOHN'.istitle()` это `False`.
- **`Field(gt=0)` на строке** — ограничение не подходит типу, Pydantic бросит ошибку при создании класса, а не при валидации данных.

## Где в репозитории

- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:20` — `positive_number = Annotated[float, Field(gt=0)]`
- `l02_pydantic_models/models.py:30` — `description: Annotated[str | None, Field(default=None, description='Description of product')]`
- `l02_pydantic_models/models.py:37` — `in_stock: Annotated[bool, Field(description='Whether product is in stock')] = False`

## См. также

[Annotated](Annotated.md), [BaseModel](BaseModel.md), [ConfigDict](ConfigDict.md)
