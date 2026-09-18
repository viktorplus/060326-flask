# load_dotenv

```python
from dotenv import load_dotenv
```

**Что это.** Читает файл `.env` и переносит его содержимое в переменные окружения процесса (`os.environ`).

**Зачем.** Настройки, которые различаются от машины к машине (пути, логины, ключи), нельзя держать в исходнике: их видно в git и они одинаковы у всех. `.env` лежит рядом с проектом и добавлен в `.gitignore`, а в репозиторий кладут только шаблон `.env.example`.

## Сигнатура

```python
load_dotenv(dotenv_path=None, stream=None, verbose=False,
            override=False, interpolate=True, encoding='utf-8') -> bool
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `dotenv_path` | str \| Path \| None | `None` | Путь к файлу. `None` — искать `.env` от текущего каталога вверх по дереву |
| `override` | bool | `False` | **Главный параметр.** `False` — НЕ трогать переменные, которые уже есть в окружении; `True` — перезаписать |
| `verbose` | bool | `False` | Печатать предупреждение, если файл не найден. Полезно при отладке «почему None» |
| `interpolate` | bool | `True` | Разворачивать ссылки вида `${OTHER}` внутри значений |
| `encoding` | str | `'utf-8'` | Кодировка файла |

## Минимальный пример

```python
import os
from dotenv import load_dotenv

# Выполнять ДО первого чтения переменных, иначе получите None.
load_dotenv()

DB_USERNAME = os.environ.get("DB_USERNAME")
print(DB_USERNAME)
```

Вывод:

```
admin
```

## Типичные задачи

**Значение обязательно — падать сразу, а не ловить None где-то глубже**

```python
import os
from dotenv import load_dotenv

load_dotenv()

try:
    SECRET = os.environ["SECRET_KEY"]      # KeyError, если ключа нет
except KeyError:
    raise SystemExit("Не задан SECRET_KEY. Скопируйте .env.example в .env")
```

**Значение с запасным вариантом и приведением типа**

```python
PORT = int(os.environ.get("PORT", 5000))   # get всегда возвращает строку
DEBUG = os.environ.get("DEBUG", "0") == "1"
```

**Свой файл для тестов**

```python
load_dotenv(dotenv_path=".env.test", override=True)
```

## Частые ошибки

- **Имя ключа совпало с системной переменной.** Самая коварная ошибка, и она реально встретилась в этом репозитории. `USERNAME` на Windows уже занят системой — там имя пользователя ОС. При `override=False` (по умолчанию) значение из `.env` будет молча отброшено, и в приложение попадёт имя пользователя Windows. Никакой ошибки при этом не возникнет. Лечение: давать ключам префикс — `DB_USERNAME`, `APP_PORT`.
- **`load_dotenv()` вызван после чтения переменных.** `os.environ.get(...)` строкой выше вернёт `None`. Порядок важен: сначала загрузка, потом чтение.
- **Файл не найден, а вы об этом не знаете.** Функция возвращает `False` и молчит. При отладке ставьте `verbose=True` либо проверяйте возвращаемое значение.
- **`.env` попал в git.** Проверить: `git check-ignore -v .env`. В репозиторий кладут только `.env.example`.
- **Все значения — строки.** `os.environ.get('DEBUG')` вернёт `'0'`, а `bool('0')` это `True`. Приводите тип явно.

## Где в репозитории

- `l03_rest_api/app.py:19` — `from dotenv import load_dotenv`
- `l03_rest_api/app.py:30` — `load_dotenv()`
- `l03_rest_api/app.py:41` — `DB_USERNAME = os.environ.get("DB_USERNAME")`
- `l03_rest_api/app.py:42` — `DRIVER = os.environ.get("DRIVER")`

## См. также

[dotenv_values](dotenv_values.md), [find_dotenv](find_dotenv.md), [set_key](set_key.md)
