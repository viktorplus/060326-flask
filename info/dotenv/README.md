# python-dotenv — справочник

Пакет из одной идеи: вынести настройки из кода в файл `.env`, который не попадает в git.

Установка: `python -m pip install python-dotenv`

В этом репозитории используется **только в `l03_rest_api/app.py`** — там читаются `DB_USERNAME` и `DRIVER`.
Шаблон значений лежит в корне репозитория: `.env.example`, его копируют в `.env`.

## Статьи

### Чтение настроек

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`load_dotenv`](load_dotenv.md) | Читает файл `. | `l03_rest_api/app.py:19`<br>`l03_rest_api/app.py:30` |
| [`dotenv_values`](dotenv_values.md) | Читает `. | — |
| [`find_dotenv`](find_dotenv.md) | Ищет файл `. | — |

### Запись настроек

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`set_key`](set_key.md) | Записывает (`set_key`) или удаляет (`unset_key`) одну переменную прямо в файле `. | — |

## Примеры

Запускаемые примеры: `cd info/dotenv && python examples.py`
