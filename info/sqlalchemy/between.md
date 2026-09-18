# .between()

```python
select(User).where(User.id.between(2, 4))
```

**Что это.** Условие «значение в диапазоне», границы ВКЛЮЧИТЕЛЬНО.

**Зачем.** Короче и читаемее, чем два условия `>=` и `<=`.

## Сигнатура

```python
колонка.between(нижняя, верхняя)
```

## Минимальный пример

```python
query = select(User).where(User.id.between(2, 4))     # id >= 2 AND id <= 4
```

## Типичные задачи

**Диапазон дат**

```python
from datetime import date
select(Employee).where(Employee.hire_date.between(date(2020, 1, 1), date(2020, 12, 31)))
```

## Частые ошибки

- **Забыть, что границы включаются.** `between(2, 4)` вернёт и 2, и 4.
- **`between` по `DateTime` для «весь день».** `between(день, день)` возьмёт только полночь. Для суток берите `>= начало дня` и `< начало следующего`.

## Где в репозитории

- `l05_orm_relationships/app.py:232` — `query = select(User).where(User.id.between(2, 4))`

## См. также

[where](where.md), [in_](in_.md)
