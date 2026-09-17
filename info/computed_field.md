# Валидаторы и вычисляемые поля
## Проверка нескольких полей

```python
@model_validator(mode="after")
def check_names_are_different(self):
    if self.first_name.lower() == self.last_name.lower():
        raise ValueError("first_name and last_name must not be the same")
    return self
```

`mode="after"` означает:

1. отдельные поля уже проверены и преобразованы;
2. создан экземпляр модели;
3. валидатор получает `self`;
4. при успехе нужно вернуть `self`.

Если условие не выполнено, внутри валидатора выбрасывают `ValueError`. Pydantic собирает его в общий `ValidationError`.

Не нужно делать так:

```python
raise ValidationError(...)
```

## `before` и `after`

| Режим | Что приходит | Когда использовать |
|---|---|---|
| `before` | сырые входные данные, часто словарь | подготовка или нормализация до проверки полей |
| `after` | готовый экземпляр модели | проверки, зависящие от нескольких уже проверенных полей |

## Вычисляемые поля

```python
@computed_field
@property
def years_worked(self) -> int:
    return calc_years_worked(self.hire_date)
```

`@property` позволяет обращаться как к атрибуту: `employee.years_worked`. `@computed_field` сообщает Pydantic, что свойство нужно учитывать при сериализации и в JSON Schema.

Порядок декораторов важен: сначала над методом стоит `@property`, а над ним `@computed_field`.

## Расчёт полного стажа

```python
def calc_years_worked(hire_date: date) -> int:
    today = date.today()
    years = today.year - hire_date.year
    anniversary_not_reached = (today.month, today.day) < (
        hire_date.month,
        hire_date.day,
    )
    return years - anniversary_not_reached
```

В арифметике Python `False == 0`, `True == 1`. Поэтому из разницы годов вычитается единица, если годовщина найма в текущем году ещё не наступила.

## Зарплата с бонусом

```python
@computed_field
@property
def actual_salary(self) -> float:
    bonus = calc_bonus_percent(self.years_worked)
    return round(self.salary * (1 + bonus), 2)
```

В проекте вычисляемые поля включаются в HTTP-ответ, но явно исключаются при сохранении в файл:

```python
e.model_dump(exclude={"years_worked", "actual_salary"})
```

