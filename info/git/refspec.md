# refspec

```python
git push origin upstream/main:refs/heads/teacher/2026-09-18
```

**Что это.** Запись `<источник>:<назначение>` — что и куда копировать. Сердце `push` и `fetch`.

**Зачем.** Именно refspec позволяет запушить **не текущую ветку**, а произвольную ссылку под произвольным именем. Без него скопировать чужую ветку в свою одной командой не выйдет.

## Сигнатура

```python
<источник>:<назначение>
+<источник>:<назначение>      # плюс = принудительно
:<назначение>                 # пустой источник = УДАЛИТЬ ветку на сервере
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `источник` | — | — | Что копируем: ветка, тег, SHA, `upstream/main`, `HEAD` |
| `назначение` | — | — | Куда: полное имя ссылки `refs/heads/<имя>` |
| ``+` в начале` | — | — | Разрешить перезапись с потерей истории (то же, что `--force`) |
| `пустой источник` | — | — | `git push origin :branch` удаляет ветку на сервере |

## Минимальный пример

```python
# Скопировать ветку main репозитория преподавателя в ветку teacher/... своего репозитория.
# Слева — ЧУЖАЯ ссылка, справа — имя НАШЕЙ новой ветки.
git push origin "upstream/main:refs/heads/teacher/2026-09-18-020000Z"
```

## Типичные задачи

**Запушить локальную ветку под другим именем**

```python
git push origin my-local-branch:refs/heads/feature-42
```

**Запушить конкретный коммит как новую ветку**

```python
git push origin 1a2b3c4:refs/heads/hotfix
```

**Удалить ветку на сервере**

```python
git push origin :refs/heads/old-branch
# то же самое понятнее:
git push origin --delete old-branch
```

## Частые ошибки

- **Короткое имя справа.** `origin/main:teacher/x` может создать не ветку, а что-то другое, если имя неоднозначно. Пишите полностью: `refs/heads/teacher/x`.
- **Перепутать стороны.** Слева — ОТКУДА берём, справа — КУДА кладём. Перепутали — и вы затрёте источник.
- **Пустой источник удаляет ветку.** Лишнее двоеточие в начале — и ветки нет. Команда при этом выглядит безобидно.

## Где в репозитории

- `.github/workflows/main.yml:100` — `REMOTE_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"`
- `.github/workflows/main.yml:106` — `git push --force-with-lease="refs/heads/$BRANCH:$REMOTE_SHA" \`
- `.github/workflows/main.yml:107` — `origin "upstream/$UPSTREAM_BRANCH:refs/heads/$BRANCH"`
- `.github/workflows/main.yml:111` — `git push origin "upstream/$UPSTREAM_BRANCH:refs/heads/$BRANCH"`

## См. также

[push](push.md), [force-with-lease](force-with-lease.md), [copy-repo-to-branch](copy-repo-to-branch.md)
