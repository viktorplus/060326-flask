# computed_field

```python
from pydantic import computed_field
```

**Что это.** Помечает свойство как поле, которое попадёт в результат сериализации, хотя в самой модели не хранится.

**Зачем.** Есть значения, которые не надо принимать от клиента и хранить: стаж считается из даты найма, итог заказа — из позиций. Хранить их — значит рисковать рассинхроном. `computed_field` считает их на лету, но они всё равно видны в JSON-ответе.

## Сигнатура

```python
@computed_field
@property
def name(self) -> тип: ...
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `return_type` | type | выводится | Тип результата. Обычно берётся из аннотации |
| `alias` | str | `None` | Имя поля в выводе |
| `repr` | bool | `True` | Показывать ли в `repr()` модели |

## Минимальный пример

```python
from datetime import date
from pydantic import BaseModel, computed_field

class Employee(BaseModel):
    hire_date: date
    salary: float

    @computed_field                 # порядок важен: computed_field СВЕРХУ
    @property
    def years_worked(self) -> int:
        today = date.today()
        return today.year - self.hire_date.year - (
            (today.month, today.day) < (self.hire_date.month, self.hire_date.day))
```

## Типичные задачи

**Исключить вычисляемые поля при сохранении в файл**

```python
# В файл-хранилище такие поля писать не нужно — они пересчитаются при чтении
data = employee.model_dump(mode='json', exclude={'years_worked', 'actual_salary'})
```

**Вычисляемое поле поверх другого вычисляемого**

```python
@computed_field
@property
def actual_salary(self) -> float:
    bonus = calc_bonus_percent(self.years_worked)   # использует соседнее computed_field
    return round(self.salary * (1 + bonus), 2)
```

## Частые ошибки

- **Перепутать порядок декораторов.** Правильно `@computed_field` сверху, `@property` под ним. Наоборот — поле в вывод не попадёт.
- **Забыть аннотацию типа результата.** Без `-> int` Pydantic не сможет построить схему.
- **Ожидать, что поле можно передать на вход.** Оно только вычисляется; попытка задать его при создании объекта будет проигнорирована или вызовет ошибку при `extra='forbid'`.
- **Сохранить вычисляемое поле в хранилище, а потом прочитать обратно.** При чтении оно пересчитается, и старое значение окажется лишним ключом. Исключайте через `exclude`.

## Где в репозитории

- `l03_rest_api/schemas.py:20` — `computed_field,   # свойство, попадающее в сериализованный вывод`
- `l03_rest_api/schemas.py:75` — `@computed_field`
- `l03_rest_api/schemas.py:82` — `@computed_field`
- `l03_rest_api/schemas.py:72` *(в закомментированном учебном блоке)* — `# @computed_field включает это свойство в model_dump()/model_dump_json(),`

## См. также

[model_dump](model_dump.md), [BaseModel](BaseModel.md), [Field](Field.md)
