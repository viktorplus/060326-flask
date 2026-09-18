# lazy (стратегии загрузки)

```python
relationship(back_populates='user', lazy='selectin')
```

**Что это.** Стратегия загрузки связи: КОГДА и СКОЛЬКИМИ запросами подтягиваются связанные объекты.

**Зачем.** Это главная тема производительности в ORM. Неудачная стратегия даёт проблему N+1: один запрос за списком плюс по одному запросу на каждый элемент.

## Сигнатура

```python
relationship(..., lazy='select' | 'joined' | 'selectin' | 'subquery' | 'raise' | 'noload')
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``'select'`` | по умолчанию | — | Отдельный запрос при первом обращении к атрибуту. **Источник проблемы N+1** |
| ``'joined'`` | — | — | Один запрос с `LEFT OUTER JOIN`. Хорошо для «многие к одному» |
| ``'selectin'`` | — | — | Два запроса: основной плюс один `WHERE id IN (...)` на все связи. Лучший выбор для «один ко многим» |
| ``'subquery'`` | — | — | Похож на `selectin`, но через подзапрос. Обычно медленнее |
| ``'raise'`` | — | — | Бросить исключение при ленивой загрузке. Способ найти N+1 в тестах |
| ``'noload'`` | — | — | Не загружать никогда; коллекция всегда пуста |

## Минимальный пример

```python
class User(Base):
    # 'selectin' — основной запрос + ОДИН запрос за всеми адресами сразу
    addresses: Mapped[list['Address']] = relationship(back_populates='user', lazy='selectin')

class Address(Base):
    # 'joined' — пользователь придёт тем же запросом, одним LEFT OUTER JOIN
    user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')
```

## Типичные задачи

**Проблема N+1 наглядно — включите echo=True и посчитайте запросы**

```python
engine = create_engine('sqlite:///db.sqlite', echo=True)

# lazy='select' (по умолчанию): 1 запрос за пользователями + по 1 на каждого
for user in session.scalars(select(User)):
    print(user, user.addresses)        # <- вот здесь уходит отдельный запрос

# lazy='selectin': всего 2 запроса независимо от числа пользователей
```

**Переопределить стратегию для конкретного запроса**

```python
from sqlalchemy.orm import selectinload, joinedload

query = select(User).options(selectinload(User.addresses))
query = select(User).options(joinedload(User.addresses))
```

**Найти N+1 в тестах**

```python
addresses: Mapped[list['Address']] = relationship(lazy='raise')
# любое неявное обращение к user.addresses теперь бросит исключение
```

## Частые ошибки

- **Обращение к связи после закрытия сессии.** При `lazy='select'` данные подгружаются в момент обращения; сессия закрыта — `DetachedInstanceError`.
- **`lazy='joined'` для «один ко многим»** размножает строки родителя и требует `distinct()`. Для коллекций лучше `selectin`.
- **Считать, что `join` заменяет стратегию загрузки.** Не заменяет: нужен `options(contains_eager(...))`.
- **Кэш сессии маскирует проблему.** Во второй раз объекты берутся из identity map, и запросов не видно. Чтобы честно померить, откройте новую сессию.

## Где в репозитории

- `l05_orm_relationships/app.py:77` — `user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')`
- `l07_orm_aggregates/app.py:56` — `user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')`
- `l08_orm_loading/app.py:30` — `addresses: Mapped[list['Address']] = relationship(back_populates='user', lazy='selectin') # 1: M`
- `l05_orm_relationships/app.py:74` *(в закомментированном учебном блоке)* — `# Обратная сторона связи. lazy='joined' — стратегия загрузки:`

## См. также

[relationship](relationship.md), [join](join.md), [sessionmaker](sessionmaker.md)
