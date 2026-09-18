# Как скопировать репозиторий в отдельную ветку

```python
git fetch upstream main
git push origin upstream/main:refs/heads/snapshot-2026-09-18
```

**Что это.** Задача: взять состояние ЧУЖОГО (или своего) репозитория и положить его в отдельную ветку своего репозитория, не трогая текущую работу.

**Зачем.** Так делают архивные снимки: сохранить урок преподавателя на дату, зафиксировать состояние перед большой переделкой, положить рядом чужой вариант для сравнения. Отдельная ветка ничего не ломает: ваша рабочая ветка и `main` остаются на месте.

## Сигнатура

```python
# Общая форма
git remote add <имя> <URL чужого репозитория>
git fetch <имя> <их ветка>
git push origin <имя>/<их ветка>:refs/heads/<ваша новая ветка>
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `Ключевая идея` | — | — | `git push` с refspec умеет отправить **любую** ссылку под **любым** именем — переключаться на неё не нужно |
| `Что НЕ меняется` | — | — | Ваша текущая ветка, рабочие файлы, `main`. Операция их не касается |
| `Истории не связаны` | — | — | Ветка-снимок имеет свою историю. Слить её с вашей можно только через `--allow-unrelated-histories` |

## Минимальный пример

```python
# 1. Объявляем чужой репозиторий под именем upstream
git remote add upstream https://github.com/cpython-projects/060326-flask

# 2. Скачиваем его ветку. Наши локальные ветки при этом НЕ меняются
git fetch upstream main

# 3. Кладём её содержимое в новую ветку нашего репозитория.
#    Слева — чужая ссылка, справа — имя нашей новой ветки
git push origin "upstream/main:refs/heads/teacher/2026-09-18"
```

## Типичные задачи

**Вариант 1. Снимок чужого репозитория в ветку своего — без переключения**

```python
git remote add upstream <URL> 2>/dev/null || git remote set-url upstream <URL>
git fetch upstream main
git push origin "upstream/main:refs/heads/snapshot-$(date -u +'%Y-%m-%d')"

# Проверить результат, ничего не скачивая:
git ls-remote --heads origin 'refs/heads/snapshot-*'
```

**Вариант 2. То же, но с локальной веткой — если снимок нужно посмотреть у себя**

```python
git fetch upstream main
git branch snapshot-2026-09-18 upstream/main     # создать, НЕ переключаясь
git push -u origin snapshot-2026-09-18

# посмотреть, не меняя рабочий каталог:
git log --oneline snapshot-2026-09-18 -5
git diff main snapshot-2026-09-18 --stat
```

**Вариант 3. Копия ТЕКУЩЕГО состояния своего репозитория в запасную ветку**

```python
# Страховка перед рискованной переделкой. Одна команда, переключаться не нужно:
git push origin "HEAD:refs/heads/backup-$(date -u +'%Y-%m-%d-%H%M%SZ')"

# Локально то же самое:
git branch backup-2026-09-18          # указатель на текущий коммит
```

**Вариант 4. Обновить уже существующую ветку-снимок — безопасно**

```python
BRANCH="teacher/2026-09-18"

# Узнаём, на каком коммите ветка сейчас
REMOTE_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"

git fetch upstream main

if [ -n "$REMOTE_SHA" ]; then
  # Перезаписываем, но только если её никто не трогал с момента проверки
  git push --force-with-lease="refs/heads/$BRANCH:$REMOTE_SHA" \
    origin "upstream/main:refs/heads/$BRANCH"
else
  git push origin "upstream/main:refs/heads/$BRANCH"
fi
```

**Вариант 5. Полная копия репозитория со всеми ветками и тегами**

```python
# Это уже не «ветка», а зеркало — нужен пустой целевой репозиторий
git clone --mirror https://github.com/cpython-projects/060326-flask
cd 060326-flask.git
git push --mirror https://github.com/<вы>/<новый-репозиторий>
```

**Автоматизация: то же самое кнопкой на вкладке Actions**

```python
# Ровно эти шаги и делает .github/workflows/main.yml этого репозитория:
#   1. actions/checkout с fetch-depth: 0
#   2. собрать и проверить имя ветки (git check-ref-format)
#   3. git remote add upstream + git fetch
#   4. git ls-remote -> создать или обновить через --force-with-lease
# Разбор по директивам: ../github-actions/README.md
```

## Частые ошибки

- **Пытаться сделать это через `git checkout` и копирование файлов.** Так теряется история, и в ветке оказывается один коммит вместо снимка. Refspec копирует ссылку целиком.
- **Забыть `git fetch` перед `push`.** Ссылки `upstream/main` ещё не существует, и push ругается на неизвестный источник.
- **Короткое имя справа от двоеточия.** Пишите `refs/heads/<имя>` — так однозначно создаётся именно ветка.
- **Слить снимок со своей веткой не получается:** `refusing to merge unrelated histories`. Это ожидаемо — у чужого репозитория своя история. Нужен `git merge --allow-unrelated-histories`, и разбирать конфликты придётся руками.
- **`--force` вместо `--force-with-lease` при обновлении снимка.** Если кто-то (или другой запуск workflow) успел изменить ветку, `--force` затрёт это молча.
- **В CI: `fetch-depth: 1`.** В поверхностном клоне нет истории, и push чужой ссылки либо упадёт, либо отправит обрезанную историю. Ставьте `fetch-depth: 0`.
- **В CI: нет `permissions: contents: write`.** `git push` вернёт 403, и выглядит это как проблема аутентификации.

## Где в репозитории

- `.github/workflows/main.yml:69` — `NAME="teacher/$(date -u +'%Y-%m-%d-%H%M%SZ')"`
- `.github/workflows/main.yml:90` — `git fetch upstream "$UPSTREAM_BRANCH"`
- `.github/workflows/main.yml:100` — `REMOTE_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"`
- `.github/workflows/main.yml:106` — `git push --force-with-lease="refs/heads/$BRANCH:$REMOTE_SHA" \`

## См. также

[push](push.md), [refspec](refspec.md), [fetch](fetch.md), [force-with-lease](force-with-lease.md), [ls-remote](ls-remote.md), [branch](branch.md)
