# render_template

```python
from flask import render_template
```

**Что это.** Рендерит шаблон Jinja2 из каталога `templates/` и возвращает готовый HTML.

**Зачем.** Когда ответ — страница для человека, а не JSON для программы. В этом курсе не используется: все уроки отдают JSON или простой текст, но в веб-приложениях это основной способ вернуть HTML.

## Сигнатура

```python
render_template(template_name_or_list, **context) -> str
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `template_name_or_list` | str \| list[str] | — | Имя файла в `templates/`. Список — взять первый существующий |
| `**context` | Any | — | Переменные, доступные внутри шаблона |

## Минимальный пример

```python
# templates/menu.html:  <h1>{{ title }}</h1>{% for d in dishes %}<li>{{ d }}</li>{% endfor %}

@app.route('/menu')
def menu():
    return render_template('menu.html', title='Меню', dishes=['суп', 'салат'])
```

## Частые ошибки

- **`TemplateNotFound`.** Шаблон ищется в `templates/` рядом с модулем, указанным в `Flask(__name__)`.
- **Экранирование.** Jinja2 по умолчанию экранирует HTML — это защита от XSS. Отключать через `|safe` только для данных, которым вы доверяете.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[Flask](Flask.md), [Response](Response.md)
