# scalar_subquery

```python
subq = select(func.avg(User.age)).scalar_subquery()
```

**Что это.** Превращает запрос в подзапрос, возвращающий ОДНО значение, — его можно подставить прямо в условие.

**Зачем.** «Пользователи старше среднего возраста» без подзапроса требуют двух обращений к базе и гонки между ними. Подзапрос делает это одним запросом.

## Сигнатура

```python
select(...).scalar_subquery()
```

## Минимальный пример

```python
from sqlalchemy import func, select

avg_age_subq = select(func.avg(User.age)).scalar_subquery()

users = session.scalars(select(User).where(User.age > avg_age_subq)).all()
```

## Типичные задачи

**Подзапрос как вычисляемая колонка**

```python
addr_count = (select(func.count(Address.id))
              .where(Address.user_id == User.id)
              .scalar_subquery())

query = select(User.username, addr_count.label('addr_count'))
```

## Частые ошибки

- **Забыть `.scalar_subquery()`.** Без него объект `Select` в условии даст предупреждение или ошибку типов.
- **Коррелированный подзапрос выполняется для КАЖДОЙ строки** — на больших таблицах это медленно; часто быстрее `join` с группировкой.

## Где в репозитории

- `l08_orm_loading/app.py:125` *(строка-комментарий)* — `#     # .scalar_subquery() помечает запрос как «возвращает одно значение»,`
- `l08_orm_loading/app.py:127` *(строка-комментарий)* — `#     avg_age_subq = select(func.avg(User.age)).scalar_subquery()`

## См. также

[select](select.md), [func](func.md), [in_](in_.md)
