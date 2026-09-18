# sessionmaker

```python
from sqlalchemy.orm import sessionmaker
```

**Что это.** Фабрика сессий, привязанная к движку. `Session` — это КЛАСС, а не объект.

**Зачем.** Сессия — «рабочая единица» (unit of work): она копит изменения в памяти и отправляет их в базу одной транзакцией. Фабрика избавляет от повторения настроек при каждом создании.

## Сигнатура

```python
Session = sessionmaker(bind=engine, autoflush=True, expire_on_commit=True)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `bind` | Engine | — | Движок, к которому привязаны сессии |
| `autoflush` | bool | `True` | Перед каждым запросом отправлять в базу накопленные изменения, чтобы запрос их увидел |
| `expire_on_commit` | bool | `True` | После `commit()` пометить объекты устаревшими: следующее обращение к полю перечитает их из базы |

## Минимальный пример

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)      # КЛАСС, вызывать через Session()

# with гарантирует закрытие сессии (возврат соединения в пул) даже при исключении
with Session() as session:
    ...
```

## Типичные задачи

**Транзакция целиком: commit при успехе, rollback при ошибке**

```python
with Session() as session, session.begin():
    session.add(User(username='admin', age=20))
    # commit произойдёт автоматически при выходе без исключения
```

**Читать поля после commit без повторного запроса**

```python
Session = sessionmaker(bind=engine, expire_on_commit=False)
```

## Частые ошибки

- **Забыть скобки: `with Session as session`.** `Session` — класс, нужен вызов `Session()`.
- **Одна сессия на всё приложение.** Сессия не потокобезопасна и копит объекты в памяти. Правильно — своя сессия на запрос или на операцию.
- **Обращение к полям объекта после выхода из `with`.** По умолчанию `expire_on_commit=True`, и после закрытия сессии поле перечитать уже негде: `DetachedInstanceError`.
- **Сессия от другого движка при базе в памяти.** У каждого движка с `:memory:` своя база — таблиц просто не окажется.

## Где в репозитории

- `l04_orm_basics/app_1.py:14` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column`
- `l04_orm_basics/app_1.py:66` — `Session = sessionmaker(bind=engine)`
- `l04_orm_basics/app_2.py:8` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, registry, Mapped, mapped_column`
- `l04_orm_basics/app_2.py:104` — `Session = sessionmaker(bind=engine)`

## См. также

[session_add](session_add.md), [session_commit](session_commit.md), [create_engine](create_engine.md)
