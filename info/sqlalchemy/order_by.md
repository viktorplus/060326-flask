# .order_by()

```python
select(User).order_by(User.age)
```

**Что это.** Задаёт порядок строк в результате.

**Зачем.** Без него порядок не гарантирован вообще — база вправе вернуть строки как ей удобно. Полагаться на «обычно приходит по id» нельзя.

## Сигнатура

```python
select(...).order_by(*columns)
```

## Минимальный пример

```python
from sqlalchemy import desc

select(User).order_by(User.age)                    # по возрастанию
select(User).order_by(desc(User.age))              # по убыванию
select(User).order_by(desc(User.age), User.username)   # сначала возраст, потом имя
select(User).order_by(User.age.desc())             # то же, методом колонки
```

## Типичные задачи

**Сортировка по вычисляемому значению**

```python
from sqlalchemy import func
query = (select(Address.city, func.count(Address.id).label('cnt'))
         .group_by(Address.city)
         .order_by(desc('cnt')))          # по имени из label
```

**NULL в конец (PostgreSQL)**

```python
select(User).order_by(User.nickname.desc().nullslast())
```

## Частые ошибки

- **Полагаться на порядок без `order_by`.** На маленькой таблице кажется, что порядок стабильный; после вставок и удалений он меняется.
- **`order_by` без `limit` на большой таблице** заставит базу отсортировать всё.
- **Сортировка строк учитывает регистр.** `'Z'` окажется раньше `'a'`. Для регистронезависимой — `func.lower(User.username)`.

## Где в репозитории

- `l05_orm_relationships/app.py:261` — `query = select(User).order_by(User.age)`
- `l05_orm_relationships/app.py:266` — `query = select(User).order_by(desc(User.age))`
- `l05_orm_relationships/app.py:272` — `query = select(User).order_by(desc(User.age), User.username)`
- `l05_orm_relationships/app.py:265` *(в закомментированном учебном блоке)* — `# desc(...) -> ORDER BY age DESC (по убыванию).`

## См. также

[select](select.md), [func](func.md), [group_by](group_by.md)
