# field_validator

```python
from pydantic import field_validator
```

**Что это.** Декоратор для собственной проверки ОДНОГО поля.

**Зачем.** Когда правило нельзя выразить через `Field`: «домен почты только из белого списка», «дата не в прошлом», «номер телефона нужного формата».

## Сигнатура

```python
@field_validator('field_name', ..., mode='after', check_fields=None)
@classmethod
def validator(cls, value): ...
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `*fields` | str | — | Имена полей. `'*'` — все поля модели |
| `mode` | str | `'after'` | `'after'` — после приведения к типу поля; `'before'` — до, значение придёт сырым |
| `check_fields` | bool | `None` | Проверять, что поле существует. Отключают для валидаторов в базовых классах |

## Минимальный пример

```python
from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    email: EmailStr

    @field_validator('email')
    @classmethod                       # ставится ПОД field_validator
    def check_email(cls, value):
        allowed = ['gmail.com', 'yahoo.com']
        _, domain = value.split('@')
        if domain not in allowed:
            raise ValueError('Invalid email address')
        return value                   # ВЕРНУТЬ ЗНАЧЕНИЕ ОБЯЗАТЕЛЬНО
```

## Типичные задачи

**Дата не в прошлом, с учётом часового пояса**

```python
from datetime import datetime

@field_validator('date')
@classmethod
def check_date(cls, value: datetime):
    # Если у значения есть tzinfo, берём "сейчас" в том же поясе,
    # иначе сравнение aware и naive бросит TypeError
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
    if value < now:
        raise ValueError('Дата не может быть в прошлом')
    return value
```

**Одно правило на несколько полей**

```python
@field_validator('first_name', 'last_name')
@classmethod
def not_empty(cls, value):
    if not value.strip():
        raise ValueError('Поле не может быть пустым')
    return value.strip()
```

**mode='before' — почистить данные ДО приведения к типу**

```python
@field_validator('price', mode='before')
@classmethod
def strip_currency(cls, value):
    if isinstance(value, str):
        return value.replace('$', '').strip()   # '$10' -> '10' -> float
    return value
```

## Частые ошибки

- **Валидатор объявлен вне тела класса.** Из-за одного уровня отступа Pydantic его просто не увидит — проверка никогда не вызовется, и модель примет любое значение. Ни ошибки, ни предупреждения. Ровно это было в задании 4 практики этого репозитория.
- **Забыть `return value`.** Валидатор должен вернуть значение; иначе в поле окажется `None`, и модель «пройдёт» проверку с пустым полем. Вторая ошибка из того же задания.
- **Бросать `ValidationError` вместо `ValueError`.** Внутри валидатора бросают `ValueError` (или `AssertionError`) — Pydantic сам завернёт его в `ValidationError` с указанием поля.
- **`@classmethod` выше `@field_validator`.** Порядок обратный: `@field_validator` сверху, `@classmethod` под ним.
- **Сравнение naive и aware дат** даёт `TypeError: can't compare offset-naive and offset-aware datetimes`. Берите `datetime.now(value.tzinfo)`.

## Где в репозитории

- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:105` — `@field_validator('email')`
- `l06_practice/app.py:9` — `from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict`
- `l06_practice/app.py:30` — `@field_validator('date')`

## См. также

[model_validator](model_validator.md), [Field](Field.md), [ValidationError](ValidationError.md)
