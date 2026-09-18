# steps

```python
steps:
  - name: ...
    uses: ...
  - name: ...
    run: ...
```

**Что это.** Шаги задачи. Выполняются СТРОГО ПОСЛЕДОВАТЕЛЬНО в одном рабочем каталоге.

**Зачем.** Шаги делят файловую систему и рабочий каталог — в отличие от задач. Поэтому склонированный на первом шаге репозиторий доступен всем следующим.

## Сигнатура

```python
steps:
  - name: <заголовок в логе>
    id: <идентификатор для ссылок>
    if: <условие>
    env: {...}
    uses: <действие>  |  run: <команды>
    with: {...}
    continue-on-error: false
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``name`` | str | — | Заголовок шага в логе |
| ``id`` | str | — | Нужен, чтобы ссылаться на выводы шага: `steps.<id>.outputs.<key>` |
| ``uses`` | str | — | Готовое действие |
| ``run`` | str | — | Команды shell |
| ``if`` | str | — | Условие выполнения шага |
| ``continue-on-error`` | bool | `false` | Не останавливать задачу при падении шага |
| ``timeout-minutes`` | int | — | Ограничение времени шага |

## Минимальный пример

```python
steps:
  - name: Checkout own repo
    uses: actions/checkout@v5
    with:
      fetch-depth: 0

  - name: Build branch name
    id: name                        # по этому id читают вывод шага
    run: |
      echo "branch=teacher/x" >> "$GITHUB_OUTPUT"
```

## Типичные задачи

**Шаг только при ручном запуске**

```python
- name: Отчёт
  if: github.event_name == 'workflow_dispatch'
  run: echo "запущено вручную"
```

**Шаг, который выполняется даже после падения предыдущего**

```python
- name: Загрузить логи
  if: always()
  uses: actions/upload-artifact@v4
```

## Частые ошибки

- **`uses` и `run` в одном шаге.** Шаг делает что-то одно — либо действие, либо команды.
- **Падение шага останавливает всю задачу.** Если это ожидаемо (например, проверка, которая может не пройти), ставьте `continue-on-error: true`.
- **Переменная из одного шага не видна в другом.** Обычный `export` живёт только внутри своего `run`. Передача — через `$GITHUB_OUTPUT` или `$GITHUB_ENV`.

## Где в репозитории

- `.github/workflows/main.yml:43` — `steps:`
- `.github/workflows/main.yml:54` — `id: name`
- `l02_pydantic_models/models.py:69` — `id: int`
- `l03_rest_api/schemas.py:42` — `id: UUID = Field(default_factory=uuid4)`

## См. также

[uses](uses.md), [run](run.md), [GITHUB_OUTPUT](GITHUB_OUTPUT.md), [jobs](jobs.md)
