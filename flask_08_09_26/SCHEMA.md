# flask_08_09_26 — схема проекта

## Что это

Первое знакомство с **SQLAlchemy ORM**. Flask здесь уже нет: оба файла — обычные скрипты,
которые выполняются сверху вниз и завершаются. HTTP-входа нет, вход у них — сам исходный код,
выход — SQL-лог в консоли и файл SQLite на диске.

| Файл | Тема |
|---|---|
| `app_1.py` | декларативная модель, создание таблиц, сессия, вставка одной записи, логирование SQL |
| `app_2.py` | три способа связать Python-класс с таблицей БД (два из трёх — закомментированы) |

## Точка входа и запуск

```
python flask_08_09_26/app_1.py
python flask_08_09_26/app_2.py
```

Строки подключения относительные (`sqlite:///db.sqlite3` и `sqlite:///db.sqlite`), поэтому файл
БД создаётся **в текущем рабочем каталоге процесса**, а не рядом со скриптом. В самом каталоге
`flask_08_09_26/` файлов БД нет: `db.sqlite3` к тому же занесён в `.gitignore` (строка 71).

## Схема

```mermaid
flowchart TB
    subgraph a1["app_1.py"]
        Log1["logging.basicConfig(level=DEBUG)<br/>logger 'sqlalchemy.engine'<br/>= аналог create_engine(echo=True)"]
        Base1["class Base(DeclarativeBase)<br/>держит metadata"]
        U1["class User(Base)<br/>__tablename__ = 'users'<br/>id PK, username VARCHAR(30), age INT"]
        E1["engine = create_engine<br/>sqlite:///db.sqlite3"]
        C1["Base.metadata.create_all(engine)<br/>создаёт недостающие таблицы"]
        S1["Session = sessionmaker(bind=engine)"]
        W1["with Session() as session:<br/>User(id=6, username='admin', age=20)<br/>session.add(...) → session.commit()"]
        Base1 --> U1 --> C1
        E1 --> C1 --> S1 --> W1
        Log1 -.->|"печатает SQL"| W1
    end

    subgraph a2["app_2.py"]
        V1["VAR 1 — императивный маппинг<br/>Table + обычный класс + map_imperatively<br/>(закомментировано)"]
        V3["VAR 3 — automap / reflection<br/>MetaData.reflect + automap_base<br/>(закомментировано)"]
        V2["VAR 2 — декларативный маппинг ← рабочий код"]
        U2["class User(Base) → 'users'<br/>id, username, age"]
        A2["class Address(Base) → 'addresses'<br/>id PK autoincrement, description VARCHAR(100)<br/>связи с users ПОКА НЕТ"]
        E2["engine = create_engine<br/>sqlite:///db.sqlite"]
        C2["Base.metadata.create_all(engine)"]
        W2["with Session() as session: pass<br/>— ни одного запроса"]
        V2 --> U2 --> C2
        V2 --> A2 --> C2
        E2 --> C2 --> W2
    end

    W1 --> DB1[("db.sqlite3<br/>в текущем каталоге<br/>(в .gitignore)")]
    W2 --> DB2[("db.sqlite<br/>в текущем каталоге<br/>таблицы users + addresses")]
    Log1 --> Console["stdout/stderr:<br/>CREATE TABLE ... / INSERT ..."]
```

## Вход / Выход

| Скрипт | Вход | Выход |
|---|---|---|
| `app_1.py` | ничего извне — данные зашиты в код: `User(id=6, username='admin', age=20)` | файл `db.sqlite3` с таблицей `users` и одной строкой; SQL-лог в консоли |
| `app_2.py` | ничего | файл `db.sqlite` с пустыми таблицами `users` и `addresses`; лога нет — логирование не настроено |

Сессия в `app_2.py` открывается и сразу закрывается (`pass`): цель урока — только факт создания
таблиц.

## Связи

Между `app_1.py` и `app_2.py` связи нет — это два независимых скрипта, у каждого свой `Base`,
свой `engine` и свой файл БД. Друг друга они не импортируют.

Внешние зависимости: `sqlalchemy` (и драйвер `sqlite3` из стандартной библиотеки).

## Особенности

* **`User(id=6, ...)` с явным id — повторный запуск `app_1.py` упадёт** с `IntegrityError`
  (нарушение уникальности первичного ключа). В коде это помечено `#!`. Если убрать `id=6`,
  SQLite подставит автоинкремент и скрипт станет идемпотентным по запуску.
* **`create_all` только создаёт недостающие таблицы.** Существующие он не изменяет: добавили
  поле в модель — в БД оно не появится. Для миграций нужен Alembic.
* **`add()` не выполняет SQL.** Он лишь помечает объект как новый в сессии; INSERT уходит в базу
  на `commit()`. Без `commit()` выход из блока `with` откатит всё.
* **Два способа включить SQL-лог эквивалентны**: `logging` с уровнем DEBUG для логгера
  `sqlalchemy.engine` (как здесь) либо `create_engine(..., echo=True)` (как в `11_09_26/app.py`).
  Уровень DEBUG показывает и запрос, и его параметры; INFO — только запрос.
* **VAR 3 (automap) достаёт класс по имени ТАБЛИЦЫ, а не класса**: `Base.classes.users`. Удобно
  для чужой/легаси-базы, но IDE не знает про поля — подсказок типов нет.
* Старый синтаксис `Column(Integer, primary_key=True)` оставлен в комментариях рядом с
  `Mapped[int] = mapped_column(...)`. Результат в БД одинаковый, разница только в подсказках
  типов для IDE и mypy.
* `Address` здесь ещё без `ForeignKey` — внешний ключ и `relationship` появляются в
  [`flask_09_09_26`](../flask_09_09_26/SCHEMA.md).
