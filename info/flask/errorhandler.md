# errorhandler

```python
@app.errorhandler(404)
def handler(e):
    ...
```

**Что это.** Регистрирует функцию, которая будет вызвана вместо стандартной страницы ошибки.

**Зачем.** В REST API любая ошибка должна приходить в том же формате, что и успешный ответ — JSON. Иначе клиент, который делает `response.json()`, упадёт на HTML-странице.

## Сигнатура

```python
@app.errorhandler(code_or_exception)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `code_or_exception` | int \| type[Exception] | — | HTTP-код (`404`) или класс исключения (`ValidationError`) |

## Минимальный пример

```python
from pydantic import ValidationError

@app.errorhandler(ValidationError)
def on_validation_error(e):
    return jsonify(e.errors(include_url=False, include_context=False)), 400

@app.errorhandler(404)
def on_not_found(e):
    return jsonify(error='not found'), 404
```

## Типичные задачи

**Единый формат ошибок для всего приложения**

```python
@app.errorhandler(Exception)
def on_any_error(e):
    code = getattr(e, 'code', 500)
    return jsonify(error=type(e).__name__, detail=str(e)), code
```

## Частые ошибки

- **Обработчик на `Exception` глотает и настоящие 500-е.** В разработке это мешает видеть traceback — логируйте исключение внутри обработчика.
- **Обработчик сам бросил исключение** — Flask отдаст 500 без подробностей.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[abort](abort.md), [jsonify](jsonify.md)
