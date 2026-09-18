# $GITHUB_OUTPUT

```python
echo "branch=$BRANCH" >> "$GITHUB_OUTPUT"
```

**Что это.** Файл, через который шаг передаёт значения следующим шагам.

**Зачем.** Каждый `run` — отдельный процесс, переменные не переживают шаг. `$GITHUB_OUTPUT` — штатный канал передачи.

## Сигнатура

```python
echo "<ключ>=<значение>" >> "$GITHUB_OUTPUT"

# читается как:
${{ steps.<id>.outputs.<ключ> }}
```

## Минимальный пример

```python
- name: Build branch name
  id: name                                   # без id читать вывод будет нечем
  run: |
    BRANCH="teacher/2026-09-18-020000Z"
    echo "branch=$BRANCH" >> "$GITHUB_OUTPUT"

- name: Use it
  env:
    BRANCH: ${{ steps.name.outputs.branch }}
  run: echo "$BRANCH"
```

## Типичные задачи

**Многострочное значение — через разделитель**

```python
run: |
  {
    echo "notes<<EOF"
    git log --oneline -5
    echo "EOF"
  } >> "$GITHUB_OUTPUT"
```

**Отдать значение из задачи в задачу**

```python
jobs:
  build:
    outputs:
      version: ${{ steps.v.outputs.version }}
    steps:
      - id: v
        run: echo "version=1.2.3" >> "$GITHUB_OUTPUT"
  deploy:
    needs: build
    steps:
      - run: echo "${{ needs.build.outputs.version }}"
```

## Частые ошибки

- **Забыть `id` у шага.** Без него обратиться к выводу невозможно — `steps..outputs` просто ничего не вернёт, молча.
- **`>` вместо `>>`.** Одна угловая скобка ЗАТРЁТ файл и потеряет выводы, записанные ранее.
- **Устаревший `::set-output name=...::`.** Он отключён GitHub; используйте `$GITHUB_OUTPUT`.
- **Многострочное значение без разделителя** ломает формат файла.

## Где в репозитории

- `.github/workflows/main.yml:80` — `echo "branch=$BRANCH" >> "$GITHUB_OUTPUT"`
- `.github/workflows/main.yml:79` *(строка-комментарий)* — `# Передаём результат следующим шагам через специальный файл $GITHUB_OUTPUT.`

## См. также

[expressions](expressions.md), [steps](steps.md), [env](env.md)
