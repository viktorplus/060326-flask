# Flask — справочник

Микрофреймворк: маршрутизация, объект запроса, объект ответа. Всё остальное — расширения.

Установка: `python -m pip install flask`

В этом репозитории Flask используется в трёх уроках:

* `l01_routing` — только маршруты и конвертеры путей, состояния нет;
* `l02_pydantic_models` — + валидация входного JSON через Pydantic, ручной `Response`;
* `l03_rest_api` — полноценный REST API: `request`, коды ответа `200/201/400`, запись в файл.

Запуск любого из них — из каталога урока: `cd l01_routing && python app.py`

## Статьи

### Приложение и маршруты

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`Flask`](Flask.md) | Класс WSGI-приложения. | `l01_routing/app.py:4`<br>`l01_routing/app.py:9` |
| [`@app.route`](route.md) | Декоратор, который связывает URL-правило с функцией-обработчиком. | `l01_routing/app.py:14`<br>`l01_routing/app.py:19` |
| [`app.run`](run.md) | Поднимает встроенный отладочный сервер Werkzeug. | `l01_routing/app.py:68`<br>`l02_pydantic_models/app.py:128` |
| [`url_for`](url_for.md) | Строит URL по имени функции-обработчика, а не по строке пути. | — |
| [`Blueprint`](Blueprint.md) | Группа маршрутов, которую регистрируют в приложении целиком. | — |

### Входящий запрос

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`request`](request.md) | Объект текущего HTTP-запроса: метод, заголовки, тело, параметры строки запроса, файлы. | `l03_rest_api/app.py:67`<br>`l03_rest_api/app.py:72` |
| [`request.get_json`](get_json.md) | Разбирает тело запроса как JSON и возвращает `dict`/`list`. | `l03_rest_api/app.py:72`<br>`l03_rest_api/app.py:103` |

### Исходящий ответ

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`jsonify`](jsonify.md) | Превращает `dict`/`list` в готовый `Response` с телом JSON и заголовком `Content-Type: application/json`. | `l02_pydantic_models/app.py:6`<br>`l02_pydantic_models/app.py:90` |
| [`Response`](Response.md) | «Ручной» объект ответа: вы сами задаёте тело, код состояния и `Content-Type`. | `l02_pydantic_models/app.py:6`<br>`l02_pydantic_models/app.py:66` |
| [`make_response`](make_response.md) | Превращает то, что вернул обработчик (строку, словарь, кортеж), в полноценный объект `Response`, который затем можно доработать. | — |
| [`render_template`](render_template.md) | Рендерит шаблон Jinja2 из каталога `templates/` и возвращает готовый HTML. | — |

### Ошибки

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`abort`](abort.md) | Немедленно прерывает обработку запроса и возвращает HTTP-ошибку. | — |
| [`errorhandler`](errorhandler.md) | Регистрирует функцию, которая будет вызвана вместо стандартной страницы ошибки. | — |

## Примеры

Запускаемые примеры: `cd info/flask && python examples.py`
