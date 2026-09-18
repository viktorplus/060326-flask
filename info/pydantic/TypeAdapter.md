# TypeAdapter

```python
from pydantic import TypeAdapter
```

**Что это.** Даёт валидацию и сериализацию для типов, которые не являются моделями: списков, словарей, union-типов, обычных `int` и `str`.

**Зачем.** `list[Employee]` — это не `BaseModel`, у него нет методов `model_validate`/`model_dump`. А принимать и отдавать массивы объектов нужно постоянно. `TypeAdapter` закрывает эту дыру.

## Сигнатура

```python
adapter = TypeAdapter(SomeType)
adapter.validate_python(obj)      adapter.validate_json(s)
adapter.dump_python(obj)          adapter.dump_json(obj, indent=4)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `type` | Any | — | Любой тип: `list[Employee]`, `dict[str, int]`, `int \| str` |
| `indent` | int | `None` | Параметр `dump_json`: отступы в выводе |

## Минимальный пример

```python
from pydantic import BaseModel, TypeAdapter

class Employee(BaseModel):
    first_name: str
    salary: float

# Создаём ОДИН раз на уровне модуля: адаптер кэширует скомпилированную схему
EmployeeListAdapter = TypeAdapter(list[Employee])

employees = EmployeeListAdapter.validate_python([
    {'first_name': 'Elena', 'salary': 80000},
    {'first_name': 'Ivan', 'salary': 50000},
])
print(EmployeeListAdapter.dump_json(employees, indent=2).decode())
```

## Типичные задачи

**Принять массив объектов одним запросом**

```python
new_employees = EmployeeListAdapter.validate_python(request.get_json(force=True))
```

**Отдать список моделей как JSON**

```python
return Response(EmployeeListAdapter.dump_json(employees, indent=4),
                mimetype='application/json')
```

**Проверить одиночное значение без модели**

```python
IntAdapter = TypeAdapter(int)
IntAdapter.validate_python('42')      # -> 42
```

## Частые ошибки

- **Создавать адаптер внутри обработчика запроса.** `TypeAdapter` компилирует схему — это дорого. Создавайте один раз на уровне модуля.
- **`dump_json` возвращает `bytes`, а не `str`.** Для печати нужен `.decode()`; во `Response` его можно передавать как есть.
- **Ожидать `model_dump` у списка.** Список — не модель; без `TypeAdapter` придётся писать `[e.model_dump() for e in items]` вручную.

## Где в репозитории

- `l02_pydantic_models/app.py:62` — `res = user.model_dump_json(indent=4)`
- `l02_pydantic_models/models.py:187` — `res = user.model_dump_json(indent=4)`
- `l03_rest_api/app.py:60` — `return Response(error.model_dump_json(indent=4), status=status, mimetype="application/json")`
- `l03_rest_api/app.py:89` — `return Response(employee.model_dump_json(indent=4), status=201, mimetype="application/json")`

## См. также

[BaseModel](BaseModel.md), [model_dump](model_dump.md), [model_validate](model_validate.md)
