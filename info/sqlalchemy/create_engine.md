# create_engine

```python
from sqlalchemy import create_engine
```

**Что это.** Создаёт «движок» — точку входа в базу: пул соединений плюс диалект конкретной СУБД.

**Зачем.** Один объект на всё приложение. Он знает, как разговаривать именно с этой базой (SQLite, PostgreSQL, MySQL) и переиспользует соединения вместо того, чтобы открывать их заново.

## Сигнатура

```python
create_engine(url, *, echo=False, echo_pool=False, pool_size=5,
              max_overflow=10, pool_pre_ping=False, future=True)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `url` | str | — | Строка подключения: `'<СУБД>+<драйвер>://<user>:<pass>@<host>:<port>/<db>'` |
| `echo` | bool | `False` | `True` — печатать весь SQL в консоль. Самый быстрый способ увидеть, что реально уходит в базу |
| `pool_size` | int | `5` | Сколько соединений держать открытыми |
| `max_overflow` | int | `10` | Сколько соединений сверх пула можно открыть при всплеске нагрузки |
| `pool_pre_ping` | bool | `False` | Проверять соединение перед выдачей. Спасает от «сервер разорвал соединение по таймауту» |

## Минимальный пример

```python
from sqlalchemy import create_engine

# Файл рядом с рабочим каталогом процесса
engine = create_engine('sqlite:///db.sqlite')

# База в оперативной памяти: живёт, пока жив процесс
engine = create_engine('sqlite:///:memory:')

# С выводом всего SQL
engine = create_engine('sqlite:///db.sqlite', echo=True)
```

## Типичные задачи

**Строки подключения к разным СУБД**

```python
'sqlite:///db.sqlite'                                   # относительный путь
'sqlite:////absolute/path/db.sqlite'                    # абсолютный: четыре слеша
'sqlite:///:memory:'                                    # в памяти
'postgresql+psycopg://user:pass@localhost:5432/mydb'
'mysql+pymysql://user:pass@localhost:3306/mydb'
```

**Собрать URL из переменных окружения, не хардкодя пароль**

```python
import os
from dotenv import load_dotenv

load_dotenv()
url = f"postgresql+psycopg://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@localhost/app"
engine = create_engine(url)
```

## Частые ошибки

- **`create_engine` НЕ открывает соединение.** Он только настраивает пул. Пока не выполнена реальная операция, к базе никто не обращался — и в логе поэтому пусто. Ровно на этом застряло задание в `l06_practice/app2.py`.
- **Относительный путь разрешается от рабочего каталога процесса, а не от файла скрипта.** Запустили не из того каталога — SQLite молча создаст новую пустую базу, и все выборки вернут пусто. Именно поэтому все уроки курса запускаются из своего каталога.
- **Число слешей в SQLite-URL.** `sqlite:///path` — относительный путь, `sqlite:////path` — абсолютный (в Unix). Лишний или недостающий слеш даёт не тот файл.
- **База в памяти и несколько движков.** Каждый движок с `:memory:` получает свою собственную базу. Сессии обязаны создаваться от того же `engine`, иначе таблиц не окажется.

## Где в репозитории

- `l04_orm_basics/app_1.py:9` — `from sqlalchemy import create_engine, Column, String, Integer`
- `l04_orm_basics/app_1.py:59` — `engine = create_engine('sqlite:///db.sqlite3')`
- `l04_orm_basics/app_2.py:5` — `from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData`
- `l04_orm_basics/app_2.py:98` — `engine = create_engine('sqlite:///db.sqlite')`

## См. также

[sessionmaker](sessionmaker.md), [create_all](create_all.md), [DeclarativeBase](DeclarativeBase.md)
