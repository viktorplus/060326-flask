# @app.route

```python
@app.route('/path')
def handler():
    ...
```

**Что это.** Декоратор, который связывает URL-правило с функцией-обработчиком.

**Зачем.** Это основной способ сказать Flask «когда придёт такой запрос — вызови вот эту функцию». Правило кладётся в `app.url_map`, а Werkzeug при запросе ищет совпадение.

## Сигнатура

```python
@app.route(rule, methods=['GET'], defaults=None, strict_slashes=None, endpoint=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `rule` | str | — | Шаблон пути. Динамические куски — в угловых скобках: `/menu/<int:id>` |
| `methods` | list[str] | `['GET']` | Разрешённые HTTP-методы. `GET` автоматически добавляет `HEAD` и `OPTIONS` |
| `defaults` | dict \| None | `None` | Значения по умолчанию для параметров правила |
| `strict_slashes` | bool \| None | `None` | `False` — считать `/menu` и `/menu/` одним и тем же адресом |
| `endpoint` | str \| None | `None` | Имя маршрута для `url_for`. По умолчанию — имя функции |

## Минимальный пример

```python
@app.route('/menu')
def menu():
    return 'Menu Page'

# int — встроенный конвертер: пропустит только цифры и отдаст в функцию int, а не str
@app.route('/menu/<int:id>')
def dish(id):
    return f'Dish id is {id}'
```

## Типичные задачи

**Конвертеры пути — встроенные типы динамических кусков**

```python
@app.route('/<string:name>')     # по умолчанию; любой текст БЕЗ слеша
@app.route('/<int:id>')          # только цифры, в функцию придёт int
@app.route('/<float:price>')     # число с точкой
@app.route('/<path:subpath>')    # как string, но слеши ВНУТРИ разрешены
@app.route('/<uuid:token>')      # UUID
@app.route('/<any(pending, active):status>')   # только из перечисленного списка
```

**Один обработчик на несколько методов**

```python
@app.route('/employees', methods=['GET', 'POST'])
def employees_view():
    if request.method == 'POST':
        ...          # создать
    ...              # вернуть список
```

**Короткие декораторы под конкретный метод (Flask 2.0+)**

```python
@app.get('/employees')
def list_employees():
    ...

@app.post('/employees')
def create_employee():
    ...
```

**Несколько правил на одну функцию**

```python
@app.route('/')
@app.route('/index')
def index():
    return 'Index Page'
```

## Частые ошибки

- **Ожидать, что маршруты проверяются в порядке объявления.** Werkzeug сортирует правила по специфичности: статический `/menu` выигрывает у динамического `/<name>`, даже если объявлен ниже. А `/menu/7` уйдёт в `<int:id>`, а не в `<category>/<sub>`.
- **`/menu/abc` при правиле `/menu/<int:id>` даёт 404, а не ошибку приложения.** Конвертер просто не совпал, и Flask ищет дальше.
- **`/a/b/c` не совпадёт с `/<category>/<sub>`.** Конвертер `string` по умолчанию не пропускает слеш. Нужен `path`.
- **Имя аргумента функции обязано совпадать с именем в правиле.** `<int:id>` требует `def dish(id)`. Иначе `TypeError` при вызове обработчика.
- **Два маршрута с одинаковым именем функции** дадут `AssertionError: View function mapping is overwriting an existing endpoint function`. Лечится параметром `endpoint`.

## Где в репозитории

- `l01_routing/app.py:14` — `@app.route('/')`
- `l01_routing/app.py:19` — `@app.route('/menu')`
- `l01_routing/app.py:27` — `@app.route('/menu/<int:id>')`
- `l01_routing/app.py:35` — `@app.route('/status/<any(pending, active):status>')`

## См. также

[Flask](Flask.md), [url_for](url_for.md), [request](request.md)
