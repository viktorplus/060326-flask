# permissions

```python
permissions:
  contents: write
```

**Что это.** Права автоматического токена `GITHUB_TOKEN` для этого запуска.

**Зачем.** Токен выдаётся каждому запуску автоматически. По умолчанию прав у него мало — и это правильно. Если workflow должен писать в репозиторий, право надо выдать явно.

## Сигнатура

```python
permissions:
  contents: read | write | none
  pull-requests: ...
  issues: ...
  packages: ...
  actions: ...
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``contents`` | — | `read` | Чтение и запись кода. **`write` нужен для `git push`** |
| ``pull-requests`` | — | `read` | Создавать и комментировать PR |
| ``issues`` | — | `read` | Работа с задачами |
| ``actions`` | — | `read` | Управление запусками |
| ``packages`` | — | `read` | Публикация пакетов |
| ``permissions: {}`` | — | — | Отобрать все права разом |

## Минимальный пример

```python
# Принцип наименьших привилегий: выдаём ровно то, без чего не обойтись.
# Здесь нужен только push в свой же репозиторий.
permissions:
  contents: write
```

## Типичные задачи

**Права для конкретной задачи, а не для всего workflow**

```python
jobs:
  snapshot:
    permissions:
      contents: write
    runs-on: ubuntu-latest
```

**Workflow только читает — отбираем всё лишнее**

```python
permissions:
  contents: read
```

## Частые ошибки

- **`Permission denied` или `403` при `git push`.** Почти всегда это отсутствующий `contents: write`. Ошибка выглядит как проблема с аутентификацией, а дело в правах токена.
- **Права по умолчанию зависят от настроек репозитория и организации.** Полагаться на них не стоит: указывайте `permissions` явно — так workflow не сломается при смене настроек.
- **`GITHUB_TOKEN` не может запускать другие workflow.** Push от него намеренно не вызывает триггер `push` — защита от бесконечного цикла. Нужен запуск по цепочке — берите Personal Access Token.

## Где в репозитории

- `.github/workflows/main.yml:24` — `permissions:`
- `.github/workflows/main.yml:27` — `contents: write`
- `.github/workflows/main.yml:25` *(строка-комментарий)* — `# contents: write нужен, чтобы шаги ниже могли делать git push в этот же репозиторий.`

## См. также

[env](env.md), [secrets](secrets.md), [jobs](jobs.md)
