# url_for

```python
from flask import url_for
```

**Что это.** Строит URL по имени функции-обработчика, а не по строке пути.

**Зачем.** Путь в одном месте — в декораторе. Если поменять `/menu` на `/dishes`, все ссылки, собранные через `url_for`, обновятся сами, а захардкоженные строки придётся искать по проекту.

## Сигнатура

```python
url_for(endpoint, *, _external=False, _scheme=None, _anchor=None, **values)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `endpoint` | str | — | Имя обработчика (по умолчанию — имя функции) или `'blueprint.function'` |
| `**values` | Any | — | Значения динамических кусков пути. Лишние уедут в строку запроса `?key=value` |
| `_external` | bool | `False` | Вернуть абсолютный URL с доменом — нужно для писем и редиректов на другой домен |
| `_anchor` | str \| None | `None` | Добавить якорь `#...` |

## Минимальный пример

```python
@app.route('/menu/<int:id>')
def dish(id):
    return f'Dish {id}'

url_for('dish', id=7)                 # '/menu/7'
url_for('dish', id=7, lang='ru')      # '/menu/7?lang=ru'
url_for('dish', id=7, _external=True) # 'http://127.0.0.1:5000/menu/7'
```

## Типичные задачи

**Ссылка на статику**

```python
url_for('static', filename='style.css')      # '/static/style.css'
```

## Частые ошибки

- **`BuildError`, если имя обработчика не найдено.** Имя — это имя функции, а не путь. Для маршрута внутри Blueprint нужно `url_for('bp_name.func_name')`.
- **Вызов вне контекста запроса** требует `app.app_context()` и заданного `SERVER_NAME`.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[route](route.md), [Blueprint](Blueprint.md)
