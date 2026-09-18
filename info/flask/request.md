# request

```python
from flask import request
```

**Что это.** Объект текущего HTTP-запроса: метод, заголовки, тело, параметры строки запроса, файлы.

**Зачем.** Всё, что прислал клиент, лежит здесь. Объект «магический» — он глобальный по виду, но на деле свой для каждого запроса и каждого потока (контекстная переменная).

## Сигнатура

```python
request.method   request.args    request.form    request.json
request.get_json()  request.headers  request.files  request.path
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `method` | str | — | HTTP-метод: `'GET'`, `'POST'`, ... |
| `args` | MultiDict | — | Параметры строки запроса: `?page=2` → `request.args['page']` |
| `form` | MultiDict | — | Тело формы (`application/x-www-form-urlencoded`) |
| `json` | Any | — | Тело как JSON. Бросает 400, если `Content-Type` не json |
| `headers` | EnvironHeaders | — | Заголовки запроса |
| `files` | MultiDict | — | Загруженные файлы |
| `path` | str | — | Путь без домена и строки запроса |

## Минимальный пример

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/employees', methods=['GET', 'POST'])
def employees_view():
    if request.method == 'POST':
        data = request.get_json(force=True)
        return {'created': data}, 201
    return {'items': []}
```

## Типичные задачи

**Параметры строки запроса с типом и значением по умолчанию**

```python
page = request.args.get('page', default=1, type=int)
tags = request.args.getlist('tag')       # ?tag=a&tag=b -> ['a', 'b']
```

**Проверить заголовок**

```python
token = request.headers.get('Authorization')
if not token:
    return {'error': 'no token'}, 401
```

## Частые ошибки

- **Обращение к `request` вне обработчика запроса** даёт `RuntimeError: Working outside of request context`. Объект существует только во время обработки запроса.
- **`request.args` — это `MultiDict`, а не `dict`.** У одного ключа может быть несколько значений; `request.args['tag']` вернёт только первое. Нужны все — `getlist`.
- **Всё из `args` и `form` приходит строками.** Приводите тип: `request.args.get('page', type=int)`.

## Где в репозитории

- `l03_rest_api/app.py:67` — `if request.method == "POST":`
- `l03_rest_api/app.py:72` — `employee = Employee(**request.get_json(force=True))`
- `l03_rest_api/app.py:103` — `new_employees = EmployeeListAdapter.validate_python(request.get_json(force=True))`
- `p03_rest_api_classwork/app.py:92` — `data = request.get_json(force=True)  # получаем данные из запроса в виде словаря`

## См. также

[get_json](get_json.md), [route](route.md), [jsonify](jsonify.md)
