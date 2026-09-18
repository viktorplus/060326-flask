# abort

```python
from flask import abort
```

**Что это.** Немедленно прерывает обработку запроса и возвращает HTTP-ошибку.

**Зачем.** Короткий выход из середины обработчика, когда дальше работать бессмысленно: ресурс не найден, нет прав, тело кривое.

## Сигнатура

```python
abort(code, *args, **kwargs) -> NoReturn
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `code` | int \| Response | — | Код ошибки: `400`, `401`, `403`, `404`, `409`, `422`, `500` |
| `description` | str | `None` | Пояснение, попадёт в тело ответа |

## Минимальный пример

```python
from flask import abort

@app.route('/employees/<uuid:emp_id>')
def get_employee(emp_id):
    employee = find(emp_id)
    if employee is None:
        abort(404, description='Сотрудник не найден')
    return jsonify(employee)
```

## Типичные задачи

**Свой JSON вместо HTML-страницы ошибки**

```python
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e.description)), 404
```

## Частые ошибки

- **Считать, что `abort` возвращает значение.** Он бросает исключение, поэтому `return abort(404)` работает, но вводит в заблуждение — код после `abort` не выполнится в любом случае.
- **По умолчанию `abort` отдаёт HTML.** Для API добавьте `@app.errorhandler`, иначе клиент, ожидающий JSON, получит страницу.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[errorhandler](errorhandler.md), [jsonify](jsonify.md)
