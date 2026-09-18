# ValidationError

```python
from pydantic import ValidationError
```

**Что это.** Исключение, которое Pydantic бросает, если данные не прошли проверку. Внутри — список всех найденных проблем, а не только первой.

**Зачем.** Клиенту API мало знать, что «что-то не так»: ему нужно, какое поле и почему. `ValidationError` несёт машиночитаемый список ошибок.

## Сигнатура

```python
try:
    Model(**data)
except ValidationError as e:
    e.errors()   # список словарей
    e.json()     # то же строкой JSON
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `errors()` | метод | — | Список словарей с ключами `type`, `loc`, `msg`, `input`, иногда `ctx` и `url` |
| `error_count()` | метод | — | Сколько ошибок найдено |
| `title` | str | — | Имя модели, на которой сломалось |

## Минимальный пример

```python
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(ge=18)

try:
    User(name='A', age=10)
except ValidationError as e:
    print(e.error_count(), 'ошибки')
    for err in e.errors():
        print(err['loc'], err['msg'])
```

Вывод:

```
2 ошибки
('name',) String should have at least 3 characters
('age',) Input should be greater than or equal to 18
```

## Типичные задачи

**Отдать ошибки клиенту в JSON**

```python
except ValidationError as e:
    return jsonify(e.errors(include_url=False, include_context=False)), 400
```

## Частые ошибки

- **`ValidationError` — наследник `ValueError`.** Поэтому `except ValueError` поймает и её. Иногда это удобно, иногда маскирует настоящую ошибку — знайте об этом.
- **Бросать `ValidationError` руками внутри валидатора.** Не надо: бросают `ValueError`, а Pydantic сам соберёт `ValidationError` с указанием поля.
- **Сериализация ошибок в JSON падает.** Разбор — в статье [errors](errors.md); в этом репозитории на этом споткнулись дважды подряд.

## Где в репозитории

- `l02_pydantic_models/app.py:9` — `from pydantic import ValidationError`
- `l02_pydantic_models/app.py:67` — `except ValidationError as e:`
- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:112` — `raise ValueError('Invalid email address')  # именно ValueError, не ValidationError`

## См. также

[errors](errors.md), [field_validator](field_validator.md), [BaseModel](BaseModel.md)
