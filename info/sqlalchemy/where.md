# .where()

```python
stmt = select(User).where(User.age > 40)
```

**Что это.** Добавляет к запросу условие `WHERE`.

**Зачем.** Фильтрация на стороне базы вместо выборки всей таблицы и отсева в Python. Разница на больших данных — на порядки.

## Сигнатура

```python
select(...).where(*criteria)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `*criteria` | — | — | Условия. Несколько аргументов или несколько вызовов — склеиваются через `AND` |

## Минимальный пример

```python
# Два .where() подряд склеиваются через AND
query = select(User).where(User.age > 40).where(User.age < 50)

# То же самое одним вызовом
query = select(User).where(User.age > 40, User.age < 50)
```

## Типичные задачи

**Операторы сравнения**

```python
select(User).where(User.age == 30)       # =
select(User).where(User.age != 30)       # !=
select(User).where(User.age > 40)        # >
select(User).where(User.age.between(20, 40))
select(User).where(User.nickname.is_(None))       # IS NULL, НЕ == None
select(User).where(User.nickname.is_not(None))    # IS NOT NULL
```

**Условие по связанной таблице**

```python
select(Address).where(Address.user_id == 1)
```

## Частые ошибки

- **Писать питоновские `and` / `or` / `not`.** SQLAlchemy 2.0 такое не пропускает: попытка вычислить истинность условия даёт `TypeError: Boolean value of this clause is not defined`. Это хорошая новость — ошибка видна сразу, а не превращается в тихо неверный фильтр. Нужны `and_()`, `or_()`, `not_()` либо несколько `.where()` подряд.
- **`== None` вместо `.is_(None)`.** Первое иногда работает, но правильный SQL для `NULL` — это `IS NULL`. Сравнение через `=` с `NULL` в SQL всегда даёт «неизвестно».
- **Забыть присвоить результат.** `.where()` возвращает новый объект запроса.
- **Думать, что `==` внутри `.where()` — это сравнение Python.** Нет: это построение SQL-условия `id = 1`. Результат — объект выражения, а не `True`/`False`.

## Где в репозитории

- `l05_orm_relationships/app.py:199` — `user_one = session.scalars(stmt.where(User.id == 1)).one()`
- `l05_orm_relationships/app.py:210` — `user_one = session.scalars(stmt.where(User.id == 1)).one_or_none()`
- `l05_orm_relationships/app.py:216` — `query = select(User).where(User.age > 40).where(User.age < 50)`
- `l05_orm_relationships/app.py:227` — `query = select(User).where(User.username.ilike('U%'))`

## См. также

[select](select.md), [or_](or_.md), [ilike](ilike.md), [in_](in_.md)
