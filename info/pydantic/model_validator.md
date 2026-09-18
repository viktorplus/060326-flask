# model_validator

```python
from pydantic import model_validator
```

**Что это.** Декоратор для проверки, которой нужны СРАЗУ НЕСКОЛЬКО полей.

**Зачем.** `field_validator` видит только своё поле. А правила вида «пароль и его повтор совпадают», «дата окончания позже даты начала», «имя и фамилия различаются» требуют доступа ко всей модели.

## Сигнатура

```python
@model_validator(mode='after')      # self — готовый объект
@model_validator(mode='before')     # values — сырые входные данные (dict)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `mode` | str | — | `'after'` — метод экземпляра, принимает `self`, все поля уже проверены. `'before'` — принимает сырой `dict` до валидации |

## Минимальный пример

```python
from pydantic import BaseModel, model_validator

class Employee(BaseModel):
    first_name: str
    last_name: str

    @model_validator(mode='after')
    def check_names_are_different(self):
        if self.first_name.lower() == self.last_name.lower():
            raise ValueError('first_name and last_name must not be the same')
        return self            # ВЕРНУТЬ self ОБЯЗАТЕЛЬНО
```

## Типичные задачи

**Пароль и подтверждение**

```python
@model_validator(mode='after')
def passwords_match(self):
    if self.password != self.password_repeat:
        raise ValueError('Пароли не совпадают')
    return self
```

**Диапазон дат**

```python
@model_validator(mode='after')
def check_period(self):
    if self.end_date <= self.start_date:
        raise ValueError('end_date должна быть позже start_date')
    return self
```

**mode='before' — достроить данные до валидации**

```python
@model_validator(mode='before')
@classmethod
def fill_full_name(cls, data: dict):
    if isinstance(data, dict) and 'full_name' not in data:
        data['full_name'] = f"{data.get('first_name','')} {data.get('last_name','')}".strip()
    return data
```

## Частые ошибки

- **Забыть `return self`** в режиме `after` — модель станет `None`.
- **В режиме `before` приходит не всегда `dict`.** Если модель создают из объекта, проверяйте `isinstance(data, dict)` перед обращением по ключу.
- **Использовать `after` там, где данные нужно чинить.** В режиме `after` поля уже приведены к типам, и если входные данные не проходят проверку типа, до валидатора дело не дойдёт.

## Где в репозитории

- `l03_rest_api/schemas.py:21` — `model_validator,  # валидатор уровня модели (видит сразу все поля)`
- `l03_rest_api/schemas.py:63` — `@model_validator(mode="after")`

## См. также

[field_validator](field_validator.md), [BaseModel](BaseModel.md)
