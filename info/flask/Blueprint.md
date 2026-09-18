# Blueprint

```python
from flask import Blueprint
```

**Что это.** Группа маршрутов, которую регистрируют в приложении целиком.

**Зачем.** Когда файл с маршрутами разрастается, его режут на части: `users.py`, `orders.py`. Blueprint позволяет объявить маршруты отдельно от `app` и подключить их одной строкой, заодно навесив общий префикс пути.

## Сигнатура

```python
Blueprint(name, import_name, url_prefix=None, template_folder=None, static_folder=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `name` | str | — | Имя группы. Входит в endpoint: `url_for('employees.list_all')` |
| `import_name` | str | — | Обычно `__name__` |
| `url_prefix` | str \| None | `None` | Общий префикс для всех маршрутов группы |

## Минимальный пример

```python
# employees.py
from flask import Blueprint, jsonify

bp = Blueprint('employees', __name__, url_prefix='/employees')

@bp.route('')
def list_all():
    return jsonify([])

# app.py
from employees import bp
app.register_blueprint(bp)
```

## Частые ошибки

- **Забыть `register_blueprint`.** Маршруты объявлены, но не подключены — везде 404.
- **`url_for('list_all')` вместо `url_for('employees.list_all')`.** Внутри Blueprint endpoint получает префикс имени группы.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[Flask](Flask.md), [route](route.md), [url_for](url_for.md)
