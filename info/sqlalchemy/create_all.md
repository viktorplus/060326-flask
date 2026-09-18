# create_all

```python
Base.metadata.create_all(engine)
```

**Что это.** Создаёт в базе все таблицы, описанные наследниками `Base`, которых там ещё нет.

**Зачем.** Быстрый старт: описали модели — получили схему. Для учебных проектов этого достаточно.

## Сигнатура

```python
Base.metadata.create_all(bind, tables=None, checkfirst=True)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `bind` | Engine | — | Движок, в котором создавать таблицы |
| `tables` | list[Table] | `None` | Создать только указанные таблицы |
| `checkfirst` | bool | `True` | Пропускать таблицы, которые уже есть. Отсюда «существующее не трогается» |

## Минимальный пример

```python
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.create_all(engine)       # CREATE TABLE users (...)
```

## Типичные задачи

**Удалить все таблицы — удобно между тестами**

```python
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
```

**Посмотреть, что вообще зарегистрировано в metadata**

```python
print(Base.metadata.tables.keys())
```

## Частые ошибки

- **Ожидать, что `create_all` изменит существующую таблицу.** Не изменит: добавили поле в модель — в базе его не появится, ошибки при этом не будет. Для изменения схемы нужен Alembic.
- **Вызвать до объявления моделей.** В `metadata` попадает только то, что уже описано; классы ниже вызова будут проигнорированы.
- **Забыть вызвать вовсе.** Тогда таблиц нет, а первый же запрос даёт `OperationalError: no such table`. И до этого момента к базе вообще никто не обращался — в логе пусто.

## Где в репозитории

- `l04_orm_basics/app_1.py:63` — `Base.metadata.create_all(engine)`
- `l04_orm_basics/app_2.py:101` — `Base.metadata.create_all(engine)`
- `l05_orm_relationships/app.py:117` — `Base.metadata.create_all(engine)`
- `l06_practice/app2.py:73` — `Base.metadata.create_all(engine)`

## См. также

[create_engine](create_engine.md), [DeclarativeBase](DeclarativeBase.md), [sessionmaker](sessionmaker.md)
