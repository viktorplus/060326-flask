# git remote

```python
git remote add upstream <URL>
git remote set-url upstream <URL>
```

**Что это.** Управляет списком удалённых репозиториев — короткими именами для длинных URL.

**Зачем.** Чтобы взять код из ЧУЖОГО репозитория, его нужно сначала объявить. `origin` — ваш форк, `upstream` — оригинал. Это соглашение, а не требование git.

## Сигнатура

```python
git remote -v                      # показать список
git remote add <имя> <url>         # добавить
git remote set-url <имя> <url>     # изменить адрес
git remote remove <имя>            # удалить
git remote rename <старое> <новое>
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``-v`` | — | — | Показать адреса: отдельно для чтения (fetch) и записи (push) |
| ``add`` | — | — | Добавить. Упадёт с ошибкой, если имя уже занято |
| ``set-url`` | — | — | Сменить адрес существующего |

## Минимальный пример

```python
# Идиома «добавить или обновить»: add падает, если remote уже есть,
# тогда по || срабатывает запасная ветка и URL просто перезаписывается.
# 2>/dev/null глушит ожидаемое сообщение об ошибке, чтобы не пугать в логе.
git remote add upstream "$UPSTREAM_URL" 2>/dev/null || \
  git remote set-url upstream "$UPSTREAM_URL"
```

## Типичные задачи

**Посмотреть, куда настроен репозиторий**

```python
git remote -v
# origin    git@github.com:viktorplus/060326-flask.git (fetch)
# origin    git@github.com:viktorplus/060326-flask.git (push)
```

**Подключить оригинал к форку**

```python
git remote add upstream https://github.com/cpython-projects/060326-flask
git fetch upstream
```

## Частые ошибки

- **`git remote add` падает, если имя занято** — `error: remote upstream already exists`. В скриптах поэтому пишут `add ... || set-url ...`.
- **Добавить remote — не значит скачать код.** После `add` нужен `git fetch`.
- **HTTPS против SSH.** Для приватного репозитория по HTTPS понадобится токен, по SSH — ключ. В CI обычно HTTPS с токеном.

## Где в репозитории

- `.github/workflows/main.yml:87` — `git remote add upstream "$UPSTREAM_URL" 2>/dev/null || \`
- `.github/workflows/main.yml:88` — `git remote set-url upstream "$UPSTREAM_URL"`
- `.github/workflows/main.yml:84` *(строка-комментарий)* — `# Добавляем remote 'upstream'. Если он уже есть, git remote add упадёт —`

## См. также

[fetch](fetch.md), [push](push.md), [copy-repo-to-branch](copy-repo-to-branch.md)
