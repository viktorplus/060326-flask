# ValidationError.errors()

```python
e.errors(include_url=False, include_context=False)
```

**Что это.** Возвращает список словарей — по одному на каждую найденную проблему.

**Зачем.** Это то, что отдают клиенту API. Но у метода есть параметры, без которых результат может оказаться несериализуемым в JSON.

## Сигнатура

```python
e.errors(*, include_url=True, include_context=True, include_input=True) -> list[dict]
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `include_url` | bool | `True` | Добавлять ссылку на документацию Pydantic в каждую ошибку. В теле ответа обычно не нужна |
| `include_context` | bool | `True` | **Ключевой параметр.** Добавлять ключ `ctx` — а в нём лежит ИСХОДНЫЙ объект исключения из валидатора, который в JSON не сериализуется |
| `include_input` | bool | `True` | Добавлять значение, которое не прошло проверку |

## Минимальный пример

```python
from pydantic import ValidationError

try:
    User(email='john.doe@example.com')
except ValidationError as e:
    for err in e.errors(include_url=False, include_context=False):
        print(err)
```

Вывод:

```
{'type': 'value_error', 'loc': ('email',), 'msg': 'Value error, Invalid email address', 'input': 'john.doe@example.com'}
```

## Типичные задачи

**Отдать ошибки из Flask — рабочий вариант**

```python
except ValidationError as e:
    return jsonify(e.errors(include_url=False, include_context=False)), 400
```

**Свести к простому виду «поле -> сообщение»**

```python
simple = {'.'.join(map(str, err['loc'])): err['msg']
          for err in e.errors(include_url=False, include_context=False)}
# {'email': 'Value error, Invalid email address'}
```

## Частые ошибки

- **`jsonify(e.errors)` без скобок.** `errors` — это МЕТОД. Без вызова в сериализацию уедет сам объект метода: `TypeError: Object of type builtin_function_or_method is not JSON serializable`.
- **`jsonify(e.errors())` со скобками, но с настройками по умолчанию.** Тоже 500: при ошибке из своего валидатора в `ctx` лежит исходный `ValueError`, а объект исключения не сериализуется: `TypeError: Object of type ValueError is not JSON serializable`. Нужен `include_context=False`.
- **Обе ошибки всплывают только тогда, когда валидация РЕАЛЬНО не прошла.** На успешном запросе код выглядит рабочим. Именно поэтому их так легко пропустить — и именно так и случилось в [l02_pydantic_models](../../l02_pydantic_models/SCHEMA.md).
- **`loc` — это кортеж, а не строка.** Для вложенных полей он выглядит как `('address', 'city')`.

## Где в репозитории

- `l02_pydantic_models/app.py:90` — `return jsonify(e.errors(include_url=False, include_context=False)), 400`
- `l03_rest_api/app.py:58` — `error = ErrorResponse(error="Validation error", details=e.errors(include_url=False, include_context=`
- `l06_practice/app.py:161` — `print(f'ValidationError (ожидаемо, дата в прошлом): {e.errors()[0]["msg"]}')`
- `p02_pydantic_classwork/app.py:67` — `return jsonify(e.errors(include_url=False, include_context=False)), 400`

## См. также

[ValidationError](ValidationError.md), [field_validator](field_validator.md)
