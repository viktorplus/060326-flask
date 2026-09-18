# model_dump

```python
data = user.model_dump()
```

**Что это.** Метод ЭКЗЕМПЛЯРА: превращает модель в словарь Python.

**Зачем.** Обратная операция к валидации. Нужна, чтобы отдать данные дальше — в шаблон, в другую библиотеку, в `json.dump`.

## Сигнатура

```python
user.model_dump(*, mode='python', include=None, exclude=None,
                by_alias=False, exclude_unset=False, exclude_none=False)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `mode` | str | `'python'` | `'python'` — оставить объекты как есть (`date`, `UUID`). `'json'` — привести к типам, которые понимает JSON |
| `include / exclude` | set | `None` | Явный список полей, которые оставить/выбросить |
| `by_alias` | bool | `False` | Использовать `alias` вместо имён полей |
| `exclude_unset` | bool | `False` | Выбросить поля, которые не задавали явно (остались по умолчанию) |
| `exclude_none` | bool | `False` | Выбросить поля со значением `None` |

## Минимальный пример

```python
print(user.model_dump())
print(user.model_dump(mode='json'))    # date -> '2018-05-01', UUID -> строка
```

## Типичные задачи

**Сохранить в файл без вычисляемых полей**

```python
data = [e.model_dump(mode='json', exclude={'years_worked', 'actual_salary'})
        for e in employees]
json.dump(data, f, indent=4, ensure_ascii=False)
```

**Частичное обновление — только заданные поля**

```python
patch = incoming.model_dump(exclude_unset=True)
# в patch попадут ТОЛЬКО те поля, которые клиент реально прислал
```

## Частые ошибки

- **`mode='python'` и `json.dump`.** `date`, `UUID`, `Decimal` останутся объектами, и `json.dump` упадёт с `TypeError: Object of type date is not JSON serializable`. Нужен `mode='json'`.
- **Сохранить вычисляемые поля в хранилище.** При следующем чтении они пересчитаются, а сохранённые значения станут лишними ключами. Исключайте их через `exclude`.

## Где в репозитории

- `l02_pydantic_models/app.py:62` — `res = user.model_dump_json(indent=4)`
- `l02_pydantic_models/models.py:187` — `res = user.model_dump_json(indent=4)`
- `l03_rest_api/app.py:60` — `return Response(error.model_dump_json(indent=4), status=status, mimetype="application/json")`
- `l03_rest_api/app.py:89` — `return Response(employee.model_dump_json(indent=4), status=201, mimetype="application/json")`

## См. также

[model_dump_json](model_dump_json.md), [computed_field](computed_field.md), [model_validate](model_validate.md)
