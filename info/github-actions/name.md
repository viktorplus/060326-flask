# name

```python
name: 1. Сохранить урок преподавателя (ibarbylev)
```

**Что это.** Имя workflow. Именно оно показывается в списке на вкладке Actions.

**Зачем.** Когда файлов workflow несколько, имя — единственное, что видит человек. Цифра в начале («1. ...») — приём сортировки: список на вкладке упорядочен по имени.

## Сигнатура

```python
name: <строка>

# у шага — своё имя:
steps:
  - name: Checkout own repo
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``name` верхнего уровня` | str | имя файла | Заголовок workflow на вкладке Actions |
| ``name` у шага` | str | текст команды | Заголовок шага в логе запуска |
| ``run-name`` | str | `name` | Имя КОНКРЕТНОГО запуска, можно собрать из переменных |

## Минимальный пример

```python
name: 1. Сохранить урок преподавателя (ibarbylev)

# Имя конкретного запуска — видно в списке запусков
run-name: Снимок от ${{ github.actor }}

jobs:
  snapshot:
    steps:
      - name: Checkout own repo      # заголовок шага в логе
        uses: actions/checkout@v5
```

## Частые ошибки

- **Нет `name` у шага.** В логе вместо понятного заголовка окажется первая строка команды — читать такой лог тяжело.
- **Имя файла и `name` не совпадают.** На вкладке Actions видно `name`, а искать файл приходится по имени в `.github/workflows/`. Держите их похожими.

## Где в репозитории

- `.github/workflows/main.yml:2` — `name: 1. Сохранить урок преподавателя (ibarbylev)`
- `.github/workflows/main.yml:14` — `branch_name:`
- `.github/workflows/main.yml:44` — `- name: Checkout own repo`
- `.github/workflows/main.yml:52` — `- name: Build branch name`

## См. также

[on](on.md), [jobs](jobs.md), [steps](steps.md)
