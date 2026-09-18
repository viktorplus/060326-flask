# model_validate_json

```python
user = User.model_validate_json(json_string)
```

**Что это.** Метод КЛАССА: за один вызов разбирает СТРОКУ JSON, проверяет её по схеме и возвращает объект модели.

**Зачем.** Без него пришлось бы делать два шага — `json.loads()`, потом `model_validate()`. Один вызов быстрее (разбор идёт в Rust-ядре) и короче.

## Сигнатура

```python
Model.model_validate_json(json_data, *, strict=None, context=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `json_data` | str \\| bytes | — | Строка или байты с JSON |
| `strict` | bool \\| None | `None` | `True` — запретить приведение типов |
| `context` | dict \\| None | `None` | Данные для валидаторов |

## Минимальный пример

```python
json_string = '''{
    "id": 1, "name": "John Doe", "age": 22.0,
    "email": "john.doe@gmail.com", "is_active": 0,
    "address": {"city": "New York", "street": "5th Avenue", "house_number": "123"}
}'''

user = User.model_validate_json(json_string, strict=False)
# strict=False (по умолчанию) разрешает "безопасные" приведения:
#   22.0 -> 22     (float в int, дробной части нет)
#   0    -> False  (int в bool)
```

## Типичные задачи

**Прочитать модель из файла**

```python
with open('employee.json', encoding='utf-8') as f:
    employee = Employee.model_validate_json(f.read())
```

## Частые ошибки

- **Вызвать на экземпляре.** Это метод класса: `User.model_validate_json(...)`, а не `user.model_validate_json(...)`.
- **Передать словарь вместо строки.** Для словаря нужен `model_validate`.
- **Удивиться приведению типов.** При `strict=False` `22.0` станет `22`, а `0` станет `False`. Если это нежелательно — `strict=True`.

## Где в репозитории

- `l02_pydantic_models/app.py:49` — `user = User.model_validate_json(json_string, strict=False)`
- `l02_pydantic_models/models.py:176` — `user = User.model_validate_json(json_string, strict=False)`
- `l02_pydantic_models/app.py:47` *(строка-комментарий)* — `# model_validate_json: разбирает СТРОКУ JSON и сразу валидирует её по модели.`
- `l02_pydantic_models/models.py:171` *(строка-комментарий)* — `# model_validate_json — метод КЛАССА: вызывается на User, а не на готовом`

## См. также

[model_validate](model_validate.md), [model_dump_json](model_dump_json.md), [BaseModel](BaseModel.md)
