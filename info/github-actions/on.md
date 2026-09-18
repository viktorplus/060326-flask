# on

```python
on:
  workflow_dispatch:
```

**Что это.** Блок, который описывает, ЧТО запускает workflow.

**Зачем.** Это единственное, что отделяет «скрипт, который кто-то когда-то запустит» от автоматизации. Без `on` workflow не выполнится никогда.

## Сигнатура

```python
on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 3 * * *'
  workflow_dispatch:
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``push`` | — | — | Запуск при отправке коммитов. Фильтруется по `branches`, `tags`, `paths` |
| ``pull_request`` | — | — | При открытии и обновлении PR |
| ``schedule`` | — | — | По расписанию cron (время UTC) |
| ``workflow_dispatch`` | — | — | Только вручную, кнопкой на вкладке Actions |
| ``workflow_call`` | — | — | Вызов из другого workflow |
| ``release`` | — | — | При публикации релиза |

## Минимальный пример

```python
# В этом репозитории — только ручной запуск: снимок урока делают, когда он нужен,
# а не при каждом коммите.
on:
  workflow_dispatch:
```

## Типичные задачи

**Запуск только при изменении определённых файлов**

```python
on:
  push:
    branches: [main]
    paths:
      - 'l0*/**'
      - '.github/workflows/**'
```

**Ежедневно по расписанию плюс возможность запустить вручную**

```python
on:
  schedule:
    - cron: '0 3 * * *'      # 03:00 UTC
  workflow_dispatch:
```

## Частые ошибки

- **`on` в YAML — это ключевое слово `true`.** По стандарту YAML 1.1 слова `on`, `off`, `yes`, `no` читаются как логические значения. GitHub это учитывает, но некоторые редакторы и линтеры подсвечивают строку странно. Пугаться не нужно.
- **`schedule` работает по UTC** и на бесплатных раннерах может запаздывать на десятки минут при высокой нагрузке.
- **Workflow с `workflow_dispatch` не появится на вкладке Actions,** пока файл не окажется в ветке по умолчанию (обычно `main`). Это частая причина «кнопки нет».

## Где в репозитории

- `.github/workflows/main.yml:9` — `on:`
- `.github/workflows/main.yml:16` — `description: 'Имя ветки. Шаблон автоматически подставит время UTC'`
- `.github/workflows/main.yml:41` — `runs-on: ubuntu-latest`
- `l02_pydantic_models/models.py:30` — `description: Annotated[str | None, Field(default=None, description='Description of product')]`

## См. также

[workflow_dispatch](workflow_dispatch.md), [jobs](jobs.md), [name](name.md)
