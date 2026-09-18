# git push

```python
git push origin <refspec>
```

**Что это.** Отправляет коммиты и ссылки в удалённый репозиторий.

**Зачем.** Единственный способ поделиться работой. С refspec умеет создавать ветки из чего угодно, не переключаясь на них.

## Сигнатура

```python
git push <remote> <refspec>
git push -u origin <ветка>        # запушить и настроить отслеживание
git push --delete origin <ветка>  # удалить ветку на сервере
git push --force-with-lease ...   # безопасная перезапись
git push --tags
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``-u` / `--set-upstream`` | — | — | Связать локальную ветку с удалённой, чтобы дальше хватало `git push` |
| ``--delete`` | — | — | Удалить ветку на сервере |
| ``--force`` | — | — | Перезаписать, **потеряв** чужие коммиты. Опасно |
| ``--force-with-lease`` | — | — | Перезаписать, только если никто не менял ветку. См. отдельную статью |
| ``--dry-run`` | — | — | Показать, что произошло бы, ничего не отправляя |
| ``--tags`` | — | — | Отправить теги |

## Минимальный пример

```python
# Обычный push: создаёт ветку teacher/... из состояния ветки преподавателя
git push origin "upstream/main:refs/heads/$BRANCH"
```

## Типичные задачи

**Первый push своей ветки**

```python
git push -u origin lernen_final
# дальше достаточно: git push
```

**Посмотреть, что уйдёт, ничего не отправляя**

```python
git push --dry-run origin main
```

**Удалить ветку на сервере**

```python
git push origin --delete teacher/2026-09-07-120314Z
```

## Частые ошибки

- **403 в CI** — почти всегда отсутствует `permissions: contents: write`, а не проблема с паролем.
- **`! [rejected] ... (fetch first)`** означает, что на сервере есть коммиты, которых нет у вас. Сначала `git fetch`, разберитесь, потом решайте — merge, rebase или `--force-with-lease`.
- **`--force` без нужды.** Он затирает чужую работу молча. Почти всегда правильный вариант — `--force-with-lease`.
- **Push ветки, на которую вы не переключены,** возможен только через refspec: `git push origin <источник>:<назначение>`.

## Где в репозитории

- `.github/workflows/main.yml:106` — `git push --force-with-lease="refs/heads/$BRANCH:$REMOTE_SHA" \`
- `.github/workflows/main.yml:111` — `git push origin "upstream/$UPSTREAM_BRANCH:refs/heads/$BRANCH"`
- `.github/workflows/main.yml:25` *(строка-комментарий)* — `# contents: write нужен, чтобы шаги ниже могли делать git push в этот же репозиторий.`

## См. также

[refspec](refspec.md), [force-with-lease](force-with-lease.md), [fetch](fetch.md), [copy-repo-to-branch](copy-repo-to-branch.md)
