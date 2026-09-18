# GitHub Actions — справочник

Автоматизация внутри GitHub: файл в `.github/workflows/`, и GitHub выполняет его на своей машине.

В этом репозитории один workflow — [`.github/workflows/main.yml`](../../.github/workflows/main.yml),
«Сохранить урок преподавателя». Он делает ровно одно: берёт текущее состояние ветки `main`
репозитория преподавателя и кладёт его в отдельную ветку `teacher/<метка времени>` этого
репозитория. К коду уроков отношения не имеет — это инструмент архивации.

**Что он делает по шагам.**

1. Клонирует этот репозиторий целиком (`fetch-depth: 0` — с полной историей).
2. Собирает имя ветки: берёт то, что ввёл человек, либо подставляет время UTC;
   гарантирует префикс `teacher/` и проверяет имя через `git check-ref-format`.
3. Добавляет remote `upstream` на репозиторий преподавателя и скачивает его ветку.
4. Смотрит через `git ls-remote`, существует ли уже такая ветка в `origin`,
   и либо создаёт её, либо перезаписывает через `--force-with-lease`.
5. Пишет итог в сводку запуска.

Практическое руководство по самой задаче — в справочнике git:
[**как скопировать репозиторий в отдельную ветку**](../git/copy-repo-to-branch.md).

**Три вещи, которые ломают workflow чаще всего.**

1. `fetch-depth: 1` по умолчанию. В поверхностном клоне нет истории, и половина команд git
   ведёт себя не так, как на машине разработчика.
2. Отсутствие `permissions: contents: write`. `git push` падает с 403, и выглядит это
   как проблема аутентификации, хотя дело в правах токена.
3. Подстановка `${{ inputs.x }}` прямо в текст `run`. Это инъекция команд; значение
   прокидывают через `env`.

## Статьи

### Структура файла

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`name`](name.md) | Имя workflow. | `.github/workflows/main.yml:2`<br>`.github/workflows/main.yml:14` |
| [`on`](on.md) | Блок, который описывает, ЧТО запускает workflow. | `.github/workflows/main.yml:9`<br>`.github/workflows/main.yml:16` |
| [`workflow_dispatch`](workflow_dispatch.md) | Триггер ручного запуска: на вкладке Actions появляется кнопка «Run workflow». | `.github/workflows/main.yml:11`<br>`.github/workflows/main.yml:13` |
| [`permissions`](permissions.md) | Права автоматического токена `GITHUB_TOKEN` для этого запуска. | `.github/workflows/main.yml:24`<br>`.github/workflows/main.yml:27` |
| [`env`](env.md) | Переменные окружения. | `.github/workflows/main.yml:30`<br>`.github/workflows/main.yml:55` |

### Задачи и шаги

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`jobs`](jobs.md) | Список задач. | `.github/workflows/main.yml:37`<br>`.github/workflows/main.yml:41` |
| [`steps`](steps.md) | Шаги задачи. | `.github/workflows/main.yml:43`<br>`.github/workflows/main.yml:54` |
| [`uses`](uses.md) | Подключает готовое действие — чужой переиспользуемый шаг из Marketplace или из репозитория. | `.github/workflows/main.yml:46`<br>`.github/workflows/main.yml:47` |
| [`actions/checkout`](actions-checkout.md) | Клонирует репозиторий в рабочий каталог задачи и настраивает git-аутентификацию. | `.github/workflows/main.yml:50`<br>`.github/workflows/main.yml:48` |
| [`run`](run.md) | Выполняет команды shell на машине-раннере. | `.github/workflows/main.yml:60`<br>`.github/workflows/main.yml:63` |

### Передача значений

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`${{ }} — выражения`](expressions.md) | Подстановка значений из контекстов GitHub. | `.github/workflows/main.yml:58`<br>`.github/workflows/main.yml:94` |
| [`$GITHUB_OUTPUT`](GITHUB_OUTPUT.md) | Файл, через который шаг передаёт значения следующим шагам. | `.github/workflows/main.yml:80`<br>`.github/workflows/main.yml:79` |
| [`$GITHUB_STEP_SUMMARY`](GITHUB_STEP_SUMMARY.md) | Файл, содержимое которого показывается как Markdown на странице запуска — над логами. | `.github/workflows/main.yml:116` |
| [`secrets`](secrets.md) | Зашифрованные значения, которые хранит GitHub и подставляет в workflow. | — |

## Примеры

Запускаемые примеры: `cd info/github-actions && python examples.py`
