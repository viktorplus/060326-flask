# request.get_json

```python
data = request.get_json(force=True)
```

**Что это.** Разбирает тело запроса как JSON и возвращает `dict`/`list`.

**Зачем.** Главный способ принять данные в REST API. В отличие от свойства `request.json`, у метода есть параметры, которые позволяют управлять поведением при неверном теле.

## Сигнатура

```python
request.get_json(force=False, silent=False, cache=True)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `force` | bool | `False` | Разбирать тело как JSON, **даже если** заголовок `Content-Type` не `application/json`. Удобно, когда клиент забыл заголовок |
| `silent` | bool | `False` | При ошибке разбора вернуть `None` вместо того, чтобы бросить 400 |
| `cache` | bool | `True` | Запомнить результат, чтобы повторный вызов не разбирал тело заново |

## Минимальный пример

```python
@app.route('/employees', methods=['POST'])
def create():
    employee = Employee(**request.get_json(force=True))
    return Response(employee.model_dump_json(), status=201, mimetype='application/json')
```

## Типичные задачи

**Мягкая обработка кривого тела — без автоматического 400**

```python
data = request.get_json(silent=True)
if data is None:
    return {'error': 'тело запроса не является корректным JSON'}, 400
```

**Проверить, что пришёл объект, а не список**

```python
data = request.get_json(force=True)
if not isinstance(data, dict):
    return {'error': 'ожидался объект JSON'}, 400
```

## Частые ошибки

- **Без `force=True` и без заголовка `Content-Type: application/json` запрос падает с 415.** Частая история при ручной проверке через curl: заголовок забыли — и непонятная ошибка.
- **`get_json()` на пустом теле бросает 400.** Если тело может быть пустым, берите `silent=True` и проверяйте на `None`.
- **`Employee(**request.get_json())` без try/except.** Любое несоответствие схеме — и обработчик упадёт с необработанным `ValidationError`, клиент получит 500 вместо 400.

## Где в репозитории

- `l03_rest_api/app.py:72` — `employee = Employee(**request.get_json(force=True))`
- `l03_rest_api/app.py:103` — `new_employees = EmployeeListAdapter.validate_python(request.get_json(force=True))`
- `p03_rest_api_classwork/app.py:92` — `data = request.get_json(force=True)  # получаем данные из запроса в виде словаря`

## См. также

[request](request.md), [jsonify](jsonify.md), [Response](Response.md)
