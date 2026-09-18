# dotenv_values

```python
from dotenv import dotenv_values
```

**Что это.** Читает `.env` и возвращает содержимое словарём, **не трогая** `os.environ`.

**Зачем.** Когда нужно посмотреть или сравнить содержимое файла, не засоряя окружение процесса. Удобно для проверок и тестов: окружение остаётся чистым.

## Сигнатура

```python
dotenv_values(dotenv_path=None, stream=None, verbose=False,
              interpolate=True, encoding='utf-8') -> OrderedDict[str, str | None]
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `dotenv_path` | str \| Path \| None | `None` | Путь к файлу |
| `interpolate` | bool | `True` | Разворачивать `${OTHER}` внутри значений |
| `encoding` | str | `'utf-8'` | Кодировка файла |

## Минимальный пример

```python
from dotenv import dotenv_values

print(dict(dotenv_values(".env")))
```

Вывод:

```
{'DB_USERNAME': 'admin', 'DRIVER': 'sqlite'}
```

## Типичные задачи

**Проверить, что шаблон и рабочий файл не разошлись по ключам**

```python
from dotenv import dotenv_values

example = set(dotenv_values(".env.example"))
actual = set(dotenv_values(".env"))

missing = example - actual
if missing:
    raise SystemExit(f"В .env не хватает ключей: {sorted(missing)}")
```

**Собрать конфигурацию из нескольких файлов**

```python
config = {
    **dotenv_values(".env.shared"),
    **dotenv_values(".env.local"),     # локальный перекрывает общий
}
```

## Частые ошибки

- **Ожидать, что после `dotenv_values()` заработает `os.environ`.** Не заработает — функция ничего не экспортирует в окружение, в этом её смысл. Для экспорта нужен `load_dotenv()`.
- **Ключ без значения даёт `None`, а не пустую строку.** Строка `FOO=` даст `{'FOO': ''}`, а строка `FOO` без знака равенства — `{'FOO': None}`.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[load_dotenv](load_dotenv.md), [find_dotenv](find_dotenv.md)
