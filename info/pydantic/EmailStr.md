# EmailStr

```python
from pydantic import EmailStr
```

**Что это.** Тип-валидатор: строка, которая обязана быть синтаксически корректным адресом электронной почты.

**Зачем.** Проверять почту регулярным выражением — классический способ ошибиться: настоящая грамматика адреса сложнее, чем кажется. Готовый тип снимает вопрос.

## Сигнатура

```python
email: EmailStr
```

## Минимальный пример

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr

User(email='john.doe@gmail.com')     # ок
User(email='not-an-email')           # ValidationError
```

## Типичные задачи

**Ограничить список доменов — это уже своя логика, нужен валидатор**

```python
@field_validator('email')
@classmethod
def check_domain(cls, value):
    _, domain = value.split('@')
    if domain not in ('gmail.com', 'yahoo.com'):
        raise ValueError('Invalid email address')
    return value
```

## Частые ошибки

- **Забыть установить зависимость.** `EmailStr` требует пакет `email-validator`: `python -m pip install 'pydantic[email]'`. Без него — `ImportError` при импорте модуля.
- **Считать, что тип проверяет существование ящика.** Проверяется только синтаксис адреса. Существует ли ящик — узнают письмом с подтверждением.
- **`str_to_upper=True` в `model_config` испортит адрес.** Он применится и к почте тоже: домены нечувствительны к регистру, а вот локальная часть — формально да.

## Где в репозитории

- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:79` — `email: Annotated[EmailStr, Field(description='Email of user')]`
- `l03_rest_api/schemas.py:17` — `EmailStr,         # валидация email`
- `l03_rest_api/schemas.py:49` — `email: EmailStr`

## См. также

[field_validator](field_validator.md), [HttpUrl](HttpUrl.md), [BaseModel](BaseModel.md)
