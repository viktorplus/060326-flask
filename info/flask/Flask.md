# Flask

```python
from flask import Flask

app = Flask(__name__)
```

**Что это.** Класс WSGI-приложения. Его экземпляр — это и есть «сайт»: он хранит таблицу маршрутов, настройки и расширения.

**Зачем.** Всё во Flask крутится вокруг одного объекта `app`. К нему цепляют маршруты (`@app.route`), обработчики ошибок, конфигурацию. Без него фреймворка нет.

## Сигнатура

```python
Flask(import_name, static_url_path=None, static_folder='static',
      template_folder='templates', instance_relative_config=False, root_path=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `import_name` | str | — | Почти всегда `__name__`. По нему Flask вычисляет корень приложения — где искать `templates/` и `static/` |
| `static_folder` | str \| None | `'static'` | Каталог со статикой (css, js, картинки). `None` — статику не раздавать |
| `static_url_path` | str \| None | `None` | URL-префикс для статики. По умолчанию совпадает с именем каталога |
| `template_folder` | str \| None | `'templates'` | Каталог с шаблонами Jinja2 |
| `instance_relative_config` | bool | `False` | Искать файлы конфигурации в каталоге `instance/`, а не в корне |

## Минимальный пример

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

if __name__ == '__main__':
    app.run()
```

## Типичные задачи

**Настройки приложения**

```python
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False      # не сортировать ключи в jsonify
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024   # лимит тела запроса, 1 МБ
```

**Посмотреть все зарегистрированные маршруты**

```python
print(app.url_map)
# или списком:
for rule in app.url_map.iter_rules():
    print(rule.rule, sorted(rule.methods))
```

## Частые ошибки

- **`Flask(__name__)` в файле, который запускают из чужого каталога.** Корень приложения считается от модуля, а вот относительные пути к данным (`open('db.json')`) — от текущего рабочего каталога. Это разные вещи, и именно поэтому все уроки курса запускаются из своего каталога.
- **Два приложения в одном процессе.** Каждое `Flask(...)` — отдельный объект со своей таблицей маршрутов. Декоратор `@app.route` цепляет маршрут только к тому `app`, у которого он вызван.

## Где в репозитории

- `l01_routing/app.py:4` — `from flask import Flask`
- `l01_routing/app.py:9` — `app = Flask(__name__)`
- `l02_pydantic_models/app.py:6` — `from flask import Flask, jsonify, Response`
- `l02_pydantic_models/app.py:18` — `app = Flask(__name__)`

## См. также

[route](route.md), [run](run.md), [Blueprint](Blueprint.md)
