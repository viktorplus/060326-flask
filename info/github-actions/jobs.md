# jobs

```python
jobs:
  snapshot:
    runs-on: ubuntu-latest
```

**Что это.** Список задач. Задачи по умолчанию выполняются ПАРАЛЛЕЛЬНО, каждая на своей машине.

**Зачем.** Разделение на задачи даёт параллельность (тесты на трёх версиях Python сразу) и изоляцию. Цена — задачи не делят файловую систему между собой.

## Сигнатура

```python
jobs:
  <id_задачи>:
    runs-on: ubuntu-latest
    needs: [другая_задача]
    if: <условие>
    strategy:
      matrix: ...
    steps: [...]
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``<id>`` | — | — | Внутренний идентификатор: буквы, цифры, `-`, `_` |
| ``runs-on`` | str | — | Машина: `ubuntu-latest`, `windows-latest`, `macos-latest` |
| ``needs`` | list | — | Ждать завершения других задач — так делается последовательность |
| ``if`` | str | — | Условие выполнения задачи |
| ``strategy.matrix`` | — | — | Размножить задачу по набору значений |
| ``outputs`` | — | — | Значения, которые задача отдаёт следующим |

## Минимальный пример

```python
jobs:
  snapshot:                    # идентификатор задачи
    runs-on: ubuntu-latest     # виртуальная машина
    steps:
      - ...
```

## Типичные задачи

**Последовательность: собрать, потом развернуть**

```python
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]
  deploy:
    needs: build               # стартует только после успешного build
    runs-on: ubuntu-latest
    steps: [...]
```

**Матрица версий**

```python
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12', '3.13']
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

## Частые ошибки

- **Ожидать, что задачи видят файлы друг друга.** Каждая задача — чистая машина. Передавать файлы между ними нужно через `actions/upload-artifact` и `download-artifact`.
- **Забыть `needs`** — задачи стартуют одновременно, и «деплой» побежит раньше «сборки».
- **`ubuntu-latest` меняется со временем.** Для воспроизводимости лучше фиксировать версию образа: `ubuntu-24.04`.

## Где в репозитории

- `.github/workflows/main.yml:37` — `jobs:`
- `.github/workflows/main.yml:41` — `runs-on: ubuntu-latest`

## См. также

[steps](steps.md), [uses](uses.md), [permissions](permissions.md)
