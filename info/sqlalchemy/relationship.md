# relationship

```python
from sqlalchemy.orm import relationship
```

**Что это.** Связь на уровне ORM: питоновский атрибут-объект вместо колонки с числом.

**Зачем.** `ForeignKey` — это связь в БАЗЕ (число в колонке). `relationship` — связь в КОДЕ: вместо `address.user_id == 5` вы пишете `address.user` и получаете готовый объект `User`. Это два разных уровня, и обычно нужны оба.

## Сигнатура

```python
relationship(argument=None, *, back_populates=None, backref=None,
             lazy='select', uselist=None, secondary=None,
             cascade='save-update, merge', order_by=None)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `argument` | str \\| type | из `Mapped` | Связанный класс. Обычно берётся из аннотации |
| `back_populates` | str | `None` | Имя парного атрибута на другой стороне. Связь объявляется явно с обеих сторон |
| `backref` | str | `None` | Старый способ: создать обратный атрибут автоматически. Менее явно, чем `back_populates` |
| `lazy` | str | `'select'` | Стратегия загрузки: `'select'`, `'joined'`, `'selectin'`, `'raise'`, `'noload'` |
| `uselist` | bool \\| None | `None` | Список или один объект. Обычно выводится из `Mapped[list[...]]` |
| `secondary` | Table | `None` | Промежуточная таблица для связи «многие ко многим» |
| `cascade` | str | `'save-update, merge'` | Что делать со связанными объектами при сохранении и удалении |
| `order_by` | — | `None` | Порядок элементов в коллекции |

## Минимальный пример

```python
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: Mapped[list['Address']] = relationship(back_populates='user')   # 1:M

class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))               # связь в БАЗЕ
    user: Mapped['User'] = relationship(back_populates='addresses')            # связь в КОДЕ
```

## Типичные задачи

**Три вида кардинальности задаются аннотацией**

```python
addresses: Mapped['Address'] = relationship(back_populates='user')            # 1:1
addresses: Mapped['Address | None'] = relationship(back_populates='user')     # 1:1 или ничего
addresses: Mapped[list['Address']] = relationship(back_populates='user')      # 1:M
```

**Каскадное заполнение: user_id расставится сам**

```python
alice = User(name='Alice', age=30, addresses=[
    Address(city='New York'),
    Address(city='Los Angeles'),
])
session.add(alice)
session.commit()       # SQLAlchemy вставит и пользователя, и оба адреса
```

**Многие ко многим через промежуточную таблицу**

```python
from sqlalchemy import Table, Column

tags_association = Table(
    'tags_association', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('tag_id', ForeignKey('tags.id')),
)

class User(Base):
    tags: Mapped[list['Tag']] = relationship(secondary=tags_association, back_populates='users')
```

**Удалять детей вместе с родителем**

```python
addresses: Mapped[list['Address']] = relationship(
    back_populates='user', cascade='all, delete-orphan')
```

## Частые ошибки

- **Забыть `ForeignKey`.** `relationship` сам по себе не создаёт связь в базе — он только описывает её в коде. Без внешнего ключа SQLAlchemy не поймёт, по каким колонкам соединять, и бросит `NoForeignKeysError`.
- **`back_populates` указан только с одной стороны** — изменения не будут отражаться во втором атрибуте до перезагрузки объекта.
- **Имя в `back_populates` — это имя АТРИБУТА, а не класса.** `back_populates='user'`, а не `back_populates='User'`.
- **Путать `join` и загрузку связи.** `select(User).join(Address)` работает как фильтр «у кого есть хотя бы один адрес», но `user.addresses` он не наполняет — за это отвечает `lazy`.

## Где в репозитории

- `l05_orm_relationships/app.py:21` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship`
- `l05_orm_relationships/app.py:48` — `addresses: Mapped[list['Address']] = relationship(back_populates='user') # 1: M`
- `l05_orm_relationships/app.py:77` — `user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')`
- `l07_orm_aggregates/app.py:14` — `from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship`

## См. также

[ForeignKey](ForeignKey.md), [lazy](lazy.md), [join](join.md), [Mapped](Mapped.md)
