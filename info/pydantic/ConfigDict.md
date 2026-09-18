# ConfigDict

```python
from pydantic import ConfigDict
```

**Что это.** Настройки поведения всей модели: что делать с пробелами, регистром, лишними полями.

**Зачем.** Правила, общие для всех полей, не нужно повторять в каждом. В Pydantic v1 для этого был внутренний класс `Config`; в v2 — атрибут `model_config`.

## Сигнатура

```python
model_config = ConfigDict(str_strip_whitespace=False, str_to_upper=False,
                          str_min_length=0, extra='ignore', frozen=False,
                          validate_assignment=False, populate_by_name=False)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `str_strip_whitespace` | bool | `False` | Обрезать пробелы по краям ВСЕХ строковых полей |
| `str_to_upper / str_to_lower` | bool | `False` | Приводить все строки к верхнему/нижнему регистру |
| `str_min_length / str_max_length` | int | `0` / `None` | Длина для всех строковых полей модели |
| `extra` | str | `'ignore'` | Лишние поля во входных данных: `'ignore'` — выбросить, `'forbid'` — ошибка, `'allow'` — сохранить |
| `validate_assignment` | bool | `False` | Проверять значение при присваивании уже созданному объекту |
| `frozen` | bool | `False` | Сделать модель неизменяемой и хешируемой |
| `populate_by_name` | bool | `False` | Разрешить заполнять поле и по имени, и по `alias` |
| `from_attributes` | bool | `False` | Позволяет собирать модель из объекта с атрибутами — например из строки SQLAlchemy |

## Минимальный пример

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,   # '  John  ' -> 'John'
        str_to_upper=True,           # 'John' -> 'JOHN'
        str_min_length=3,
    )
    name: str

print(User(name='   John   ').name)
```

Вывод:

```
JOHN
```

## Типичные задачи

**Не пропускать лишние поля — защита от опечаток в API**

```python
model_config = ConfigDict(extra='forbid')
# {'nmae': 'John'} -> ValidationError: Extra inputs are not permitted
```

**Проверять и при изменении объекта**

```python
model_config = ConfigDict(validate_assignment=True)
user.age = 999       # теперь ValidationError, а не молчаливое присваивание
```

**Собрать модель из объекта SQLAlchemy**

```python
model_config = ConfigDict(from_attributes=True)
schema = UserSchema.model_validate(orm_user)     # читает атрибуты, а не ключи
```

## Частые ошибки

- **Внутренний класс назван `ConfigDict`, а не `Config`.** В v1 конфигурация задавалась классом с именем ровно `Config`; класс с другим именем просто игнорируется — ошибки не будет, настройки молча не применятся. В v2 правильный способ один: атрибут `model_config`.
- **Ожидать, что настройки распространятся на вложенные модели.** Не распространятся: `str_min_length=3` у `User` не действует на `Address`, поэтому `city='NY'` (2 символа) пройдёт.
- **`frozen=True` и попытка изменить поле** дают `ValidationError`, а не `AttributeError`.

## Где в репозитории

- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:62` — `model_config = ConfigDict(`
- `l03_rest_api/schemas.py:16` — `ConfigDict,       # настройки поведения модели`
- `l03_rest_api/schemas.py:37` — `model_config = ConfigDict(str_strip_whitespace=True)`

## См. также

[BaseModel](BaseModel.md), [Field](Field.md)
