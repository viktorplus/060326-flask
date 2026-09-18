# env

```python
env:
  UPSTREAM_URL: https://github.com/cpython-projects/060326-flask
```

**Что это.** Переменные окружения. Задаются на трёх уровнях: всего workflow, одной задачи, одного шага.

**Зачем.** Значение, которое встречается в нескольких шагах, держат в одном месте. А ещё через `env` безопасно прокидывают пользовательский ввод в shell — см. «Частые ошибки».

## Сигнатура

```python
env:              # весь workflow
jobs:
  job:
    env: ...   # одна задача
    steps:
      - env: ...  # один шаг
```

## Минимальный пример

```python
env:
  UPSTREAM_URL: https://github.com/cpython-projects/060326-flask
  UPSTREAM_BRANCH: main

# в шаге читается как обычная переменная окружения
run: git fetch upstream "$UPSTREAM_BRANCH"
```

## Типичные задачи

**Прокинуть ввод пользователя в shell безопасно**

```python
- name: Build branch name
  env:
    BRANCH_NAME_INPUT: ${{ inputs.branch_name }}     # подстановка ВНЕ текста скрипта
  run: |
    NAME="$BRANCH_NAME_INPUT"                        # внутри скрипта — обычная переменная
```

**Передать значение между шагами через файл окружения**

```python
- run: echo "VERSION=1.2.3" >> "$GITHUB_ENV"
- run: echo "$VERSION"        # видно в СЛЕДУЮЩИХ шагах
```

## Частые ошибки

- **Подставлять `${{ inputs.x }}` прямо в текст `run`.** Это инъекция команд: значение вставляется в скрипт ДО запуска, и ввод вида `foo"; rm -rf /; "` выполнится как команда. Правильно — через `env`, как сделано в этом workflow.
- **Ожидать, что `$GITHUB_ENV` подействует в ТЕКУЩЕМ шаге.** Нет: только в следующих.
- **Класть секреты в `env` верхнего уровня.** Они попадут во все шаги, включая сторонние действия. Передавайте секрет только тому шагу, которому он нужен.

## Где в репозитории

- `.github/workflows/main.yml:30` — `env:`
- `.github/workflows/main.yml:55` — `env:`
- `.github/workflows/main.yml:92` — `env:`

## См. также

[expressions](expressions.md), [secrets](secrets.md), [GITHUB_OUTPUT](GITHUB_OUTPUT.md)
