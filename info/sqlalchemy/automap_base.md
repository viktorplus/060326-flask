# automap_base

```python
from sqlalchemy.ext.automap import automap_base
```

**Что это.** Строит классы моделей автоматически, прочитав схему уже существующей базы.

**Зачем.** Для чужой или унаследованной базы, где описывать десятки таблиц руками дорого. Схема читается на лету, классы появляются сами.

## Сигнатура

```python
Base = automap_base(metadata=metadata)
Base.prepare()
Model = Base.classes.<имя_таблицы>
```

## Минимальный пример

```python
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base

engine = create_engine('sqlite:///db.sqlite3')
metadata = MetaData()
metadata.reflect(bind=engine)      # прочитать схему из базы

Base = automap_base(metadata=metadata)
Base.prepare()

User = Base.classes.users          # по имени ТАБЛИЦЫ, а не класса
user = User(id=6, username='admin', age=20)
```

## Частые ошибки

- **Класс берётся по имени ТАБЛИЦЫ.** `Base.classes.users`, а не `Base.classes.User`.
- **Нет подсказок типов.** IDE ничего не знает о полях — классы построены во время работы программы.
- **Таблица без первичного ключа не отобразится.** Automap пропустит её молча.
- **Забыть `metadata.reflect(bind=engine)`** — `Base.classes` окажется пустым.

## Где в репозитории

- `l04_orm_basics/app_2.py:11` — `from sqlalchemy.ext.automap import automap_base`
- `l04_orm_basics/app_2.py:10` *(в закомментированном учебном блоке)* — `# automap_base — автоматически строит классы по УЖЕ существующим таблицам в БД.`
- `l04_orm_basics/app_2.py:66` *(в закомментированном учебном блоке)* — `# Base = automap_base(metadata=metadata)`

## См. также

[registry](registry.md), [DeclarativeBase](DeclarativeBase.md), [Table](Table.md)
