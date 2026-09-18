# Annotated

```python
from typing import Annotated
```

**Что это.** Способ «приклеить» метаданные к типу: `Annotated[тип, метаданные]`. Для Python это по-прежнему исходный тип, а Pydantic читает приклеенное.

**Зачем.** Два способа записать ограничение — `x: int = Field(ge=18)` и `x: Annotated[int, Field(ge=18)]`. Второй лучше: значение по умолчанию остаётся справа от знака `=`, а ограничения — в типе. Главное — такой тип можно объявить один раз и переиспользовать в разных моделях.

## Сигнатура

```python
Annotated[базовый_тип, метаданные, ...]
```

## Минимальный пример

```python
from typing import Annotated
from pydantic import BaseModel, Field

# Правило описано один раз и работает в любой модели
positive_number = Annotated[float, Field(gt=0)]

class Product(BaseModel):
    name: str
    price: positive_number

class Order(BaseModel):
    total: positive_number
```

## Типичные задачи

**Ограничение и значение по умолчанию одновременно**

```python
description: Annotated[str | None, Field(default=None, description='Описание товара')] = None
```

**Тип с готовым валидатором из annotated_types**

```python
from annotated_types import Len

Tags = Annotated[list[str], Len(min_length=1, max_length=5)]
```

## Частые ошибки

- **Задать значение по умолчанию в двух местах сразу** — и внутри `Field(default=...)`, и после знака `=`. Работает, но сбивает с толку: держите его в одном месте.
- **Путать с `Optional`.** `Optional[int]` это «int или None», а `Annotated[int, ...]` — «int с дополнительной информацией». Разные вещи.

## Где в репозитории

- `l02_pydantic_models/models.py:4` — `from typing import Annotated`
- `l02_pydantic_models/models.py:20` — `positive_number = Annotated[float, Field(gt=0)]`
- `l02_pydantic_models/models.py:30` — `description: Annotated[str | None, Field(default=None, description='Description of product')]`
- `l02_pydantic_models/models.py:37` — `in_stock: Annotated[bool, Field(description='Whether product is in stock')] = False`

## См. также

[Field](Field.md), [BaseModel](BaseModel.md)
