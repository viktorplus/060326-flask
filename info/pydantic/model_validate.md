# model_validate

```python
user = User.model_validate(data)
```

**Что это.** Метод КЛАССА: собирает и проверяет модель из готового объекта Python — обычно `dict`.

**Зачем.** Данные чаще всего уже разобраны в словарь (например, `request.get_json()`). Метод класса, а не экземпляра, потому что экземпляра ещё нет — он как раз и создаётся.

## Сигнатура

```python
Model.model_validate(obj, *, strict=None, from_attributes=None, context=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `obj` | Any | — | Словарь или объект с атрибутами |
| `strict` | bool \\| None | `None` | `True` — запретить приведение типов: `'22'` больше не станет `22` |
| `from_attributes` | bool \\| None | `None` | Читать атрибуты объекта, а не ключи словаря. Для строк SQLAlchemy |
| `context` | dict \\| None | `None` | Произвольные данные, доступные валидаторам через `info.context` |

## Минимальный пример

```python
data = {'id': 1, 'name': 'John', 'age': 20,
        'address': {'city': 'NY', 'street': 'Main', 'house_number': '10'}}

user = User.model_validate(data)
```

## Типичные задачи

**Собрать схему из объекта SQLAlchemy**

```python
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str

schema = UserSchema.model_validate(orm_user)
```

**Строгий режим — без «безопасных» приведений**

```python
User.model_validate({'age': '20'}, strict=True)   # ValidationError: не int
```

## Частые ошибки

- **`User(**data)` против `model_validate(data)`.** Первое падает с `TypeError`, если в словаре ключ — не идентификатор Python. Второе работает всегда и понятнее читается.
- **Забыть `from_attributes=True` при работе с ORM** — `ValidationError`, потому что Pydantic попытается читать объект как словарь.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[model_validate_json](model_validate_json.md), [model_dump](model_dump.md), [BaseModel](BaseModel.md)
