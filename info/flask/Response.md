# Response

```python
from flask import Response
```

**Что это.** «Ручной» объект ответа: вы сами задаёте тело, код состояния и `Content-Type`.

**Зачем.** Нужен, когда тело уже готово в виде строки и повторно сериализовать его нельзя — например, `model_dump_json()` у Pydantic уже вернул строку JSON, и `jsonify` её только испортит.

## Сигнатура

```python
Response(response=None, status=None, headers=None, mimetype=None,
         content_type=None, direct_passthrough=False)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `response` | str \| bytes \| iterable | `None` | Тело ответа |
| `status` | int \| str | `200` | Код состояния: `201`, `404`, `'404 NOT FOUND'` |
| `headers` | dict \| list | `None` | Дополнительные заголовки |
| `mimetype` | str \| None | `None` | Тип содержимого без кодировки: `'application/json'`, `'text/html'` |
| `content_type` | str \| None | `None` | Полный заголовок вместе с кодировкой: `'application/json; charset=utf-8'` |

## Минимальный пример

```python
from flask import Response

@app.route('/')
def index():
    res = user.model_dump_json(indent=4)      # это уже СТРОКА JSON
    return Response(res, mimetype='application/json')
```

## Типичные задачи

**Ответ 201 при создании ресурса**

```python
return Response(employee.model_dump_json(indent=4),
                status=201,
                mimetype='application/json')
```

**Отдать обычный текст или CSV**

```python
return Response('id;name\n1;admin\n', mimetype='text/csv')
```

**Свой заголовок**

```python
return Response(body, mimetype='application/json',
                headers={'X-Total-Count': str(total)})
```

## Частые ошибки

- **Забыть `mimetype`.** Тело уедет как `text/html`, и клиент (или браузерный `fetch().json()`) не поймёт, что это JSON.
- **Спутать `mimetype` и `content_type`.** Задавать оба сразу не нужно: `content_type` перекрывает.
- **Отдать в `Response` словарь.** Он превратится в строку через `str()` — получится не JSON, а питоновское представление с одинарными кавычками.

## Где в репозитории

- `l02_pydantic_models/app.py:6` — `from flask import Flask, jsonify, Response`
- `l02_pydantic_models/app.py:66` — `return Response(res, mimetype='application/json')`
- `l03_rest_api/app.py:13` — `from flask import Flask, Response, request`
- `l03_rest_api/app.py:26` — `from schemas import Employee, EmployeeListAdapter, ErrorResponse`

## См. также

[jsonify](jsonify.md), [make_response](make_response.md), [get_json](get_json.md)
