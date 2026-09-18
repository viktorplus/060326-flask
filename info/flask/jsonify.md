# jsonify

```python
from flask import jsonify
```

**Что это.** Превращает `dict`/`list` в готовый `Response` с телом JSON и заголовком `Content-Type: application/json`.

**Зачем.** Ручная сборка ответа (`json.dumps` + `Response`) — три строки и шанс забыть mimetype. `jsonify` делает это одним вызовом и правильно обрабатывает кодировку.

## Сигнатура

```python
jsonify(*args, **kwargs) -> Response
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `*args` | dict \| list \| Any | — | Один объект — сериализуется он. Несколько — соберутся в список |
| `**kwargs` | Any | — | `jsonify(a=1, b=2)` эквивалентно `jsonify({'a': 1, 'b': 2})` |

## Минимальный пример

```python
from flask import jsonify

@app.route('/ping')
def ping():
    return jsonify(status='ok', version=1)
    # -> {"status": "ok", "version": 1}  с mimetype application/json
```

## Типичные задачи

**Ответ с кодом состояния — возвращаем кортеж**

```python
return jsonify({'error': 'not found'}), 404
return jsonify(employee), 201
```

**Отдать ошибки валидации Pydantic**

```python
except ValidationError as e:
    # include_context=False обязателен: иначе в ctx поедет объект исключения,
    # который не сериализуется в JSON
    return jsonify(e.errors(include_url=False, include_context=False)), 400
```

## Частые ошибки

- **Передать в `jsonify` объект, который не сериализуется.** `TypeError: Object of type X is not JSON serializable`. В этом репозитории так ловили сразу две ошибки: сначала `jsonify(e.errors)` (без скобок — улетал объект метода), потом `jsonify(e.errors())` (в `ctx` лежал `ValueError`). Разбор — в [l02_pydantic_models/SCHEMA.md](../../l02_pydantic_models/SCHEMA.md).
- **Передать в `jsonify` готовую строку JSON.** Она будет экранирована и уедет как строка, а не как объект. Для готовой строки нужен `Response(..., mimetype='application/json')`.
- **Забыть код ответа.** `return jsonify({'error': ...})` отдаёт 200 — клиент не отличит успех от отказа, не разбирая тело.

## Где в репозитории

- `l02_pydantic_models/app.py:6` — `from flask import Flask, jsonify, Response`
- `l02_pydantic_models/app.py:90` — `return jsonify(e.errors(include_url=False, include_context=False)), 400`
- `l02_pydantic_models/app.py:4` *(в закомментированном учебном блоке)* — `# jsonify      — превращает dict/list в готовый Response с mimetype application/json.`
- `l02_pydantic_models/app.py:64` *(в закомментированном учебном блоке)* — `# Отдаём готовую строку как JSON-ответ. jsonify здесь не подходит:`

## См. также

[Response](Response.md), [make_response](make_response.md), [get_json](get_json.md)
