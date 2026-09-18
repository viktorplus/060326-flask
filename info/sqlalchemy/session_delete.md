# session.delete

```python
session.delete(obj)
session.commit()
```

**Что это.** Помечает объект на удаление. SQL уходит в базу на `commit()` (или `flush()`).

**Зачем.** Это удаление «по правилам ORM»: срабатывают каскады, связанные объекты обрабатываются так, как описано в `relationship`.

## Сигнатура

```python
session.delete(instance)
```

## Минимальный пример

```python
user = session.scalar(select(User).where(User.name == 'Alice'))
if user:
    session.delete(user)
    session.commit()
```

## Типичные задачи

**Удаление с каскадом по связи**

```python
class User(Base):
    addresses: Mapped[list['Address']] = relationship(
        back_populates='user', cascade='all, delete-orphan')

# Удаляем пользователя — его адреса уходят вместе с ним:
# адресов в базе было 7, стало 5 (у Alice их было 2). Проверено.
session.delete(user)
session.commit()
```

**Удалить по условию, не загружая объекты**

```python
from sqlalchemy import delete
session.execute(delete(User).where(User.age < 18))    # каскады ORM НЕ сработают
```

## Частые ошибки

- **Каскад по умолчанию детей НЕ удаляет — он их ОТВЯЗЫВАЕТ.** Значение по умолчанию `'save-update, merge'` при удалении родителя выставляет внешний ключ ребёнка в `NULL`: уходит `UPDATE addresses SET user_id=NULL`. Дальше два исхода, и оба плохие. Колонка объявлена `NOT NULL` — получите `IntegrityError: NOT NULL constraint failed`. Колонка nullable — ошибки не будет, и в базе останутся осиротевшие строки без родителя; это хуже, потому что ломается тихо. Оба случая воспроизведены в `examples.py`, раздел 22. Лечение: `cascade='all, delete-orphan'` в `relationship` либо `ondelete='CASCADE'` у `ForeignKey`. И помните: SQLite по умолчанию внешние ключи не проверяет — нужен `PRAGMA foreign_keys=ON`.
- **Ожидать, что объект после удаления «испортится».** Распространённое заблуждение. Проверено запуском: после `delete` + `commit` объект переходит в состояние **detached**, но уже загруженные значения остаются при нём — и `user.id`, и `user.name` читаются без ошибки, в том числе после закрытия сессии. `DetachedInstanceError` возникнет только при обращении к полю, которого в объекте нет: перечитать его неоткуда. Сохранять `id` заранее стоит ради читаемости, а не из-за исключения.
- **Забыть `commit()`** — выход из блока `with` откатит удаление, и запись останется.
- **`session.delete(None)`** даёт `AttributeError`: результат выборки надо проверять.

## Где в репозитории

- `l09_orm_practice/app.py:101` — `session.delete(user_to_delete)`
- `l09_orm_practice/app.py:94` *(строка-комментарий)* — `# после session.delete + commit объект переходит в состояние detached,`

## См. также

[bulk_update_delete](bulk_update_delete.md), [session_commit](session_commit.md), [relationship](relationship.md), [ForeignKey](ForeignKey.md)
