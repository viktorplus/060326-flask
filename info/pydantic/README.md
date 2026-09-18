# Pydantic v2 — справочник

Библиотека проверки данных. Модель описывается аннотациями типов, а Pydantic по ним строит
валидацию и сериализацию — ядро написано на Rust, поэтому это ещё и быстро.

Установка: `python -m pip install pydantic "pydantic[email]"`

В этом репозитории Pydantic используется в трёх уроках:

* `l02_pydantic_models` — типы, `Field`, `ConfigDict`, `field_validator`, наследование;
* `l03_rest_api` — `model_validator`, `computed_field`, `TypeAdapter`, ошибки в ответе API;
* `l06_practice` — четыре учебных задания на модели и валидаторы.

**Мнемоника методов.** `model_validate*` — методы КЛАССА: объекта ещё нет, он создаётся.
`model_dump*` — методы ЭКЗЕМПЛЯРА: сериализуется состояние конкретного объекта.
Суффикс `_json` означает работу со строкой JSON, без суффикса — со словарём Python.

## Статьи

### Основа

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`BaseModel`](BaseModel.md) | Базовый класс всех моделей. | `l02_pydantic_models/models.py:13`<br>`l02_pydantic_models/models.py:24` |
| [`Field`](Field.md) | Описывает ограничения и метаданные одного поля: границы чисел, длину строк, значение по умолчанию, описание для документации. | `l02_pydantic_models/models.py:13`<br>`l02_pydantic_models/models.py:20` |
| [`Annotated`](Annotated.md) | Способ «приклеить» метаданные к типу: `Annotated[тип, метаданные]`. | `l02_pydantic_models/models.py:4`<br>`l02_pydantic_models/models.py:20` |
| [`ConfigDict`](ConfigDict.md) | Настройки поведения всей модели: что делать с пробелами, регистром, лишними полями. | `l02_pydantic_models/models.py:13`<br>`l02_pydantic_models/models.py:62` |

### Своя проверка

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`field_validator`](field_validator.md) | Декоратор для собственной проверки ОДНОГО поля. | `l02_pydantic_models/models.py:13`<br>`l02_pydantic_models/models.py:105` |
| [`model_validator`](model_validator.md) | Декоратор для проверки, которой нужны СРАЗУ НЕСКОЛЬКО полей. | `l03_rest_api/schemas.py:21`<br>`l03_rest_api/schemas.py:63` |
| [`computed_field`](computed_field.md) | Помечает свойство как поле, которое попадёт в результат сериализации, хотя в самой модели не хранится. | `l03_rest_api/schemas.py:20`<br>`l03_rest_api/schemas.py:75` |

### Готовые типы-валидаторы

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`EmailStr`](EmailStr.md) | Тип-валидатор: строка, которая обязана быть синтаксически корректным адресом электронной почты. | `l02_pydantic_models/models.py:13`<br>`l02_pydantic_models/models.py:79` |
| [`HttpUrl`](HttpUrl.md) | Тип-валидатор: строка, которая обязана быть корректной ссылкой `http://` или `https://`. | `l02_pydantic_models/models.py:13`<br>`l02_pydantic_models/models.py:43` |

### Ввод: разбор и проверка

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`model_validate`](model_validate.md) | Метод КЛАССА: собирает и проверяет модель из готового объекта Python — обычно `dict`. | — |
| [`model_validate_json`](model_validate_json.md) | Метод КЛАССА: за один вызов разбирает СТРОКУ JSON, проверяет её по схеме и возвращает объект модели. | `l02_pydantic_models/app.py:49`<br>`l02_pydantic_models/models.py:176` |
| [`TypeAdapter`](TypeAdapter.md) | Даёт валидацию и сериализацию для типов, которые не являются моделями: списков, словарей, union-типов, обычных `int` и `str`. | `l02_pydantic_models/app.py:62`<br>`l02_pydantic_models/models.py:187` |

### Вывод: сериализация

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`model_dump`](model_dump.md) | Метод ЭКЗЕМПЛЯРА: превращает модель в словарь Python. | `l02_pydantic_models/app.py:62`<br>`l02_pydantic_models/models.py:187` |
| [`model_dump_json`](model_dump_json.md) | Метод ЭКЗЕМПЛЯРА: превращает модель сразу в СТРОКУ JSON. | `l02_pydantic_models/app.py:62`<br>`l02_pydantic_models/models.py:187` |

### Ошибки

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`ValidationError`](ValidationError.md) | Исключение, которое Pydantic бросает, если данные не прошли проверку. | `l02_pydantic_models/app.py:9`<br>`l02_pydantic_models/app.py:67` |
| [`ValidationError.errors()`](errors.md) | Возвращает список словарей — по одному на каждую найденную проблему. | `l02_pydantic_models/app.py:90`<br>`l03_rest_api/app.py:58` |

## Примеры

Запускаемые примеры: `cd info/pydantic && python examples.py`
