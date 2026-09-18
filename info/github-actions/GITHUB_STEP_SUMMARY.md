# $GITHUB_STEP_SUMMARY

```python
echo "### Snapshot created: \`$BRANCH\`" >> "$GITHUB_STEP_SUMMARY"
```

**Что это.** Файл, содержимое которого показывается как Markdown на странице запуска — над логами.

**Зачем.** Логи длинные, и итог в них теряется. Сводка отвечает на вопрос «что сделал этот запуск» без раскрытия логов.

## Сигнатура

```python
echo "<markdown>" >> "$GITHUB_STEP_SUMMARY"
```

## Минимальный пример

```python
# Обратные слеши экранируют кавычки Markdown внутри двойных кавычек bash
echo "### Snapshot $ACTION: \`$BRANCH\`" >> "$GITHUB_STEP_SUMMARY"
```

## Типичные задачи

**Таблица в сводке**

```python
{
  echo "| Ветка | Действие |"
  echo "|---|---|"
  echo "| \`$BRANCH\` | $ACTION |"
} >> "$GITHUB_STEP_SUMMARY"
```

## Частые ошибки

- **`>` вместо `>>`** затирает всё, что записали предыдущие шаги.
- **Секрет в сводке.** Она видна всем, у кого есть доступ к Actions. GitHub маскирует известные ему секреты, но собранные строки может и не распознать.
- **Предел 1 МБ** на сводку одного шага.

## Где в репозитории

- `.github/workflows/main.yml:116` — `echo "### Snapshot $ACTION: \`$BRANCH\`" >> "$GITHUB_STEP_SUMMARY"`

## См. также

[run](run.md), [GITHUB_OUTPUT](GITHUB_OUTPUT.md)
