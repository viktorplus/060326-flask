# make_response

```python
from flask import make_response
```

**Что это.** Превращает то, что вернул обработчик (строку, словарь, кортеж), в полноценный объект `Response`, который затем можно доработать.

**Зачем.** Когда ответ уже сформирован, но нужно добавить заголовок или cookie. Без него пришлось бы собирать `Response` с нуля.

## Сигнатура

```python
make_response(*args) -> Response
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `*args` | str \| dict \| tuple \| Response | — | То же, что можно вернуть из обработчика: тело, `(тело, код)`, `(тело, код, заголовки)` |

## Минимальный пример

```python
from flask import make_response

@app.route('/hello')
def hello():
    resp = make_response('Hello', 200)
    resp.headers['X-Powered-By'] = 'Flask'
    return resp
```

## Типичные задачи

**Установить cookie**

```python
resp = make_response(jsonify(ok=True))
resp.set_cookie('session_id', '123', httponly=True, max_age=3600)
return resp
```

## Частые ошибки

- **Забыть вернуть результат.** `make_response(...)` сам по себе ничего не отправляет — его нужно вернуть из обработчика.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[Response](Response.md), [jsonify](jsonify.md)
