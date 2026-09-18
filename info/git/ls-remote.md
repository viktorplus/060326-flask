# git ls-remote

```python
git ls-remote --heads origin "refs/heads/$BRANCH"
```

**Что это.** Спрашивает у сервера список ссылок и их SHA. Ничего не скачивает и не меняет.

**Зачем.** Способ узнать, существует ли ветка на сервере и на каком она коммите, не клонируя репозиторий. В скриптах — основной приём «создать или обновить».

## Сигнатура

```python
git ls-remote [--heads|--tags] <remote> [<шаблон>]
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``--heads`` | — | — | Только ветки |
| ``--tags`` | — | — | Только теги |
| ``--exit-code`` | — | — | Код возврата 2, если ничего не найдено — удобно для `if` |
| ``<шаблон>`` | — | — | Фильтр: `refs/heads/teacher/*` |

## Минимальный пример

```python
# Узнаём, существует ли такая ветка в origin, и берём её текущий SHA.
# awk 'NR == 1 { print $1 }' — первая колонка первой строки вывода.
# Если ветки нет, вывод пустой и REMOTE_SHA останется пустой строкой.
REMOTE_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"

if [ -n "$REMOTE_SHA" ]; then
  echo "ветка есть, она на $REMOTE_SHA"
else
  echo "ветки нет"
fi
```

Вывод:

```
fd6ee157a54e62e7751943266b309262c436b5ea	refs/heads/teacher/2026-09-07-120314Z
```

## Типичные задачи

**Все снимки уроков на сервере**

```python
git ls-remote --heads origin 'refs/heads/teacher/*'
```

**Проверка через код возврата вместо разбора вывода**

```python
if git ls-remote --exit-code --heads origin "refs/heads/$BRANCH" >/dev/null 2>&1; then
  echo "ветка существует"
fi
```

## Частые ошибки

- **Вывод — две колонки через табуляцию:** SHA и полное имя ссылки. Нужен только SHA — берите первую колонку через `awk` или `cut -f1`.
- **Пустой вывод — это НЕ ошибка.** Код возврата остаётся `0`, просто строк нет. Поэтому проверяют непустоту переменной (`[ -n "$X" ]`) либо ставят `--exit-code`.
- **Короткое имя вместо полного.** Пишите `refs/heads/<ветка>`: шаблон `<ветка>` может совпасть и с тегом.

## Где в репозитории

- `.github/workflows/main.yml:100` — `REMOTE_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"`
- `.github/workflows/main.yml:98` *(строка-комментарий)* — `# awk 'NR == 1 {print $1}' — первая колонка первой строки вывода ls-remote.`

## См. также

[push](push.md), [force-with-lease](force-with-lease.md), [copy-repo-to-branch](copy-repo-to-branch.md)
