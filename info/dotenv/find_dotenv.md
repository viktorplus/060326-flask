# find_dotenv

```python
from dotenv import find_dotenv
```

**Что это.** Ищет файл `.env`, поднимаясь по дереву каталогов вверх, и возвращает найденный путь строкой.

**Зачем.** Скрипт можно запустить из любого места, а `.env` лежит в корне проекта. `find_dotenv()` избавляет от относительных путей вида `../../.env`.

## Сигнатура

```python
find_dotenv(filename='.env', raise_error_if_not_found=False, usecwd=False) -> str
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `filename` | str | `'.env'` | Имя искомого файла |
| `raise_error_if_not_found` | bool | `False` | Бросить `IOError` вместо возврата пустой строки |
| `usecwd` | bool | `False` | Искать от текущего рабочего каталога, а не от файла, вызвавшего функцию |

## Минимальный пример

```python
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))
```

## Типичные задачи

**Надёжная загрузка независимо от каталога запуска**

```python
from dotenv import load_dotenv, find_dotenv

path = find_dotenv(usecwd=True)
if not path:
    raise SystemExit("Файл .env не найден. Скопируйте .env.example в .env")
load_dotenv(path)
```

## Частые ошибки

- **Пустая строка вместо пути.** Если файл не найден, функция по умолчанию возвращает `''`, а `load_dotenv('')` тихо ничего не делает. Ставьте `raise_error_if_not_found=True`.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[load_dotenv](load_dotenv.md), [dotenv_values](dotenv_values.md)
