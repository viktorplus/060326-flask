# exists / any / has

```python
from sqlalchemy import exists

select(User).where(User.addresses.any())
```

**Что это.** Условие «существует хотя бы одна связанная строка». В SQL — `EXISTS (...)`.

**Зачем.** Вопрос «у кого есть хотя бы один адрес» через `join` требует `distinct()` и всё равно тащит лишние строки. `EXISTS` останавливается на первом совпадении и дубликатов не даёт.

## Сигнатура

```python
Model.коллекция.any(критерий=None)     # 1:M — есть хотя бы один
Model.объект.has(критерий=None)        # M:1 — связанный объект подходит
exists().where(условие)                # ручная сборка
~Model.коллекция.any()                 # NOT EXISTS
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``.any()`` | — | — | Для коллекции (`Mapped[list[...]]`). Без аргумента — «есть хоть что-то» |
| ``.any(критерий)`` | — | — | «есть связанная строка, удовлетворяющая условию» |
| ``.has()`` | — | — | Для одиночной связи (`Mapped['User']`) |
| ``~`` | — | — | Отрицание: `NOT EXISTS`. Питоновский `not` здесь не работает |

## Минимальный пример

```python
from sqlalchemy import select

# У кого есть хотя бы один адрес
with_addr = select(User).where(User.addresses.any())

# У кого адресов нет вообще
without = select(User).where(~User.addresses.any())
```

Вывод:

```
с адресами : [U(Alice,30), U(Bob,22), U(Carol,30), U(Eve,27), U(Frank,45)]
без адресов: [U(Dave,17)]
```

## Типичные задачи

**Есть связанная строка с условием**

```python
# У кого есть адрес в Берлине
select(User).where(User.addresses.any(Address.city == 'Berlin'))
```

**Со стороны «многие к одному» — has()**

```python
# Адреса пользователей старше 40
select(Address).where(Address.user.has(User.age > 40))
```

**Ручная сборка, когда relationship нет**

```python
from sqlalchemy import exists

subq = exists().where(Address.user_id == User.id)
select(User).where(subq)
```

## Частые ошибки

- **Питоновский `not` вместо `~`.** `not User.addresses.any()` потребует привести условие к `bool` и даст `TypeError: Boolean value of this clause is not defined`.
- **`join` вместо `EXISTS` для вопроса «есть ли».** `select(User).join(Address)` вернёт пользователя столько раз, сколько у него адресов, — понадобится `distinct()`. `any()` этой проблемы лишён по устройству.
- **`.any()` на одиночной связи** — там нужен `.has()`, и наоборот.
- **`EXISTS` не даёт доступа к полям связанной таблицы** в `SELECT`: он только фильтрует. Нужны сами адреса — придётся соединять.

## Где в репозитории

- В коде уроков не встречается: символ добавлен как популярный за пределами курса.

## См. также

[join](join.md), [distinct](distinct.md), [subquery](subquery.md), [where](where.md)
