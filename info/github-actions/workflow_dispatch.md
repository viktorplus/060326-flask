# workflow_dispatch

```python
on:
  workflow_dispatch:
    inputs:
      branch_name:
        ...
```

**Что это.** Триггер ручного запуска: на вкладке Actions появляется кнопка «Run workflow».

**Зачем.** Есть действия, которые нельзя выполнять автоматически: они что-то перезаписывают или стоят денег. Снимок чужого репозитория — как раз такое: он нужен по решению человека.

## Сигнатура

```python
on:
  workflow_dispatch:
    inputs:
      <имя_поля>:
        description: ...
        required: true
        default: ...
        type: string | boolean | choice | environment
```

## Минимальный пример

```python
on:
  workflow_dispatch:
    inputs:
      branch_name:
        description: 'Имя ветки. Шаблон автоматически подставит время UTC'
        required: true
        default: 'teacher/YYYY-MM-DD-HHMMSSZ'
        type: string
```

## Типичные задачи

**Выбор из списка вместо свободного ввода**

```python
inputs:
  environment:
    description: 'Куда разворачиваем'
    required: true
    type: choice
    options: [staging, production]
```

**Флажок**

```python
inputs:
  dry_run:
    description: 'Только показать, что будет сделано'
    type: boolean
    default: true
```

## Частые ошибки

- **Кнопки «Run workflow» нет.** Файл должен лежать в ветке по умолчанию. Пока workflow только в рабочей ветке, запустить его вручную нельзя.
- **`type: boolean` приходит в shell строкой `'true'`/`'false'`.** Сравнивайте со строкой: `if [ "$DRY_RUN" = "true" ]`, а не как с логическим значением.
- **`default` как значение-заглушка.** В этом workflow по умолчанию стоит `teacher/YYYY-MM-DD-HHMMSSZ` — это не рабочее значение, а подсказка формата. Скрипт отдельно проверяет, не осталась ли заглушка, и подставляет реальное время.
- **Не более 10 полей ввода** — ограничение GitHub.

## Где в репозитории

- `.github/workflows/main.yml:11` — `workflow_dispatch:`
- `.github/workflows/main.yml:13` — `inputs:`
- `.github/workflows/main.yml:16` — `description: 'Имя ветки. Шаблон автоматически подставит время UTC'`
- `.github/workflows/main.yml:18` — `required: true`

## См. также

[on](on.md), [expressions](expressions.md), [run](run.md)
