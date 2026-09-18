# model_dump_json

```python
s = user.model_dump_json(indent=4)
```

**Что это.** Метод ЭКЗЕМПЛЯРА: превращает модель сразу в СТРОКУ JSON.

**Зачем.** Короче, чем `json.dumps(model.model_dump(mode='json'))`, и правильно обрабатывает специальные типы — `date`, `UUID`, `Decimal`, `HttpUrl`.

## Сигнатура

```python
user.model_dump_json(*, indent=None, include=None, exclude=None,
                     by_alias=False, exclude_unset=False, exclude_none=False)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `indent` | int \\| None | `None` | Отступы для человекочитаемого вывода |
| `include / exclude` | set | `None` | Какие поля оставить/выбросить |
| `by_alias` | bool | `False` | Использовать `alias` вместо имён полей |

## Минимальный пример

```python
res = user.model_dump_json(indent=4)
return Response(res, mimetype='application/json')
```

## Типичные задачи

**Отдать модель из Flask**

```python
# jsonify здесь НЕ подходит: он ждёт dict/list, а у нас уже готовая строка
return Response(employee.model_dump_json(indent=4), status=201,
                mimetype='application/json')
```

## Частые ошибки

- **Передать результат в `jsonify`.** Строка будет экранирована и уедет как строка, а не как объект JSON. Для готовой строки нужен `Response(..., mimetype='application/json')`.
- **Путать с `model_dump`.** `model_dump` возвращает `dict`, `model_dump_json` — `str`. Мнемоника: `model_validate_json` — метод КЛАССА (объекта ещё нет), `model_dump_json` — метод ЭКЗЕМПЛЯРА (сериализуем состояние конкретного объекта).

## Где в репозитории

- `l02_pydantic_models/app.py:62` — `res = user.model_dump_json(indent=4)`
- `l02_pydantic_models/models.py:187` — `res = user.model_dump_json(indent=4)`
- `l03_rest_api/app.py:60` — `return Response(error.model_dump_json(indent=4), status=status, mimetype="application/json")`
- `l03_rest_api/app.py:89` — `return Response(employee.model_dump_json(indent=4), status=201, mimetype="application/json")`

## См. также

[model_dump](model_dump.md), [model_validate_json](model_validate_json.md), [TypeAdapter](TypeAdapter.md)
