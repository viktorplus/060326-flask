# l02_pydantic_models — схема проекта

## Что это

Первое знакомство с **Pydantic v2**: описание моделей, ограничения полей, вложенные модели,
собственные валидаторы, наследование — и ручная отдача `Response` из Flask.

Проект состоит из двух модулей: `models.py` (модели + демонстрационный код, выполняющийся
при импорте) и `app.py` (Flask поверх них). Постоянного хранилища нет — «входные данные»
зашиты в исходник как строка JSON.

## Точка входа и запуск

```
cd l02_pydantic_models
python app.py
```

Запускать нужно **из каталога `l02_pydantic_models`**: в `app.py` стоит абсолютный импорт
`from models import User`, а не `from .models import User`. Из корня проекта модуль `models`
не найдётся.

`app.run(debug=True)` → `http://127.0.0.1:5000` с автоперезагрузкой и отладочной страницей ошибок.

## Схема

```mermaid
flowchart TB
    Client["HTTP-клиент"] -->|"GET /"| Index

    subgraph app["app.py"]
        Index["index()<br/>json_string зашит в код"]
        Menu["/menu → menu()"]
        Dish["/menu/&lt;int:id&gt; → dish(id)"]
        Status["/status/&lt;any(pending,active)&gt;<br/>→ check_status()"]
        Cat["/&lt;category&gt;/&lt;sub&gt; → dish_cat()"]
        Events["/events → events()"]
    end

    subgraph models["models.py — Pydantic"]
        User["User<br/>id, name, age, email,<br/>is_active, address"]
        Address["Address<br/>city, street, house_number"]
        Admin["Admin(User)<br/>+ is_admin"]
        Product["Product"]
        Order["Order"]
        Cfg["model_config:<br/>str_strip_whitespace<br/>str_to_upper<br/>str_min_length=3"]
        Val["@field_validator('email')<br/>домен ∈ gmail.com, yahoo.com"]
        Demo["Код верхнего уровня:<br/>создаёт user_1, разбирает json_string,<br/>печатает результат в stdout"]
        User --> Address
        User --> Cfg
        User --> Val
        Admin --> User
    end

    Index -->|"import models<br/>(Demo выполняется здесь же)"| models
    Index -->|"User.model_validate_json"| User
    Index -->|"успех"| OK["Response(<br/>user.model_dump_json(indent=4),<br/>mimetype=application/json)"]
    Index -->|"ValidationError"| Err["jsonify(e.errors) ← учебный баг"]

    OK --> Client
    Err --> Client
    Menu --> Txt["text/html: простая строка"]
    Dish --> Txt
    Status --> Txt
    Cat --> Txt
    Events --> Txt
    Txt --> Client
```

## Вход / Выход

| Маршрут | Вход | Выход |
|---|---|---|
| `/` | **ничего от клиента** — JSON зашит в тело функции `index()` | `application/json`: сериализованный `User` с `age`, увеличенным на 10 |
| `/menu` | — | `Menu of MyCafe` |
| `/menu/<int:id>` | `id` как `int` | `Dish id is 5` |
| `/status/<any(pending, active):status>` | `status` ∈ {`pending`, `active`} | `status is active` |
| `/<category>/<sub>` | два сегмента пути | `Dish category is fish and sub is soup` |
| `/events` | — | `Events of MyCafe` |

Побочный выход: `models.py` при импорте печатает в **stdout сервера** результат своей
демонстрации (см. ниже), а `index()` дополнительно печатает туда же `print(user)`.

### Что делает Pydantic на входе (`strict=False`)

| Поле в JSON | Значение | После валидации | Почему |
|---|---|---|---|
| `age` | `22.0` (float) | `22` (int) | нестрогий режим допускает `float → int` без потерь |
| `is_active` | `0` (int) | `False` | нестрогий режим допускает `int → bool` |
| `name` | `"John Doe"` | `"JOHN DOE"` | `str_to_upper=True` из `model_config` |
| `address` | вложенный объект | экземпляр `Address` | вложенная модель |

## Связи

```
app.py  ──import──▶  models.py  ──▶  pydantic
   │
   └──▶ flask (Flask, jsonify, Response)
```

Внешние зависимости: `flask`, `pydantic`, `email-validator` (нужен для `EmailStr`).
Файлов данных и БД нет. `__init__.py` пустой — только маркер пакета.

## Особенности и учебные баги

* **Ветка `except`: две ошибки подряд, обе исправлены.** Разобраны прямо в коде, неправильные
  варианты оставлены закомментированными.
  1. `jsonify(e.errors)` — `errors` это метод, а не свойство. Без скобок в `jsonify` попадёт
     сам объект метода: `TypeError: Object of type builtin_function_or_method is not JSON
     serializable`.
  2. `jsonify(e.errors())` — со скобками, но всё равно 500. По умолчанию `errors()` кладёт в
     каждый элемент ключ `ctx` с **исходным исключением** валидатора (здесь — `ValueError` из
     `check_email`), а объект исключения не сериализуется: `TypeError: Object of type
     ValueError is not JSON serializable`. Именно поэтому в
     [`l03_rest_api`](../l03_rest_api/SCHEMA.md) стоит `include_context=False`.

  Рабочий вариант: `jsonify(e.errors(include_url=False, include_context=False)), 400`.
  Код ответа добавлен там же: без него Flask вернул бы `200`, и клиент не отличил бы
  успех от отказа, не разобрав тело.
* **Демонстрационный код в `models.py` закрыт защитой `if __name__ == '__main__'`.** Раньше он
  выполнялся при каждом импорте: `app.py` делает `from models import User`, и при старте сервера
  в консоль уходил `ValidationError: ...` — легко принять за сбой приложения. Правило общее:
  в модуле с моделями кода верхнего уровня быть не должно. Примеры никуда не делись,
  запустить их отдельно: `python models.py`.
* **Демонстрация в `models.py` намеренно падает.** `json_string` там содержит
  `john.doe@example.com`, а `check_email` разрешает только `gmail.com` и `yahoo.com` —
  это и показывает работу валидатора. В `app.py` домен, наоборот, проходящий
  (`john.doe@gmail.com`), чтобы маршрут `/` отдавал успешный ответ; подставьте любой другой
  домен — и увидите ветку `except`.
* **`user.age += 10` не проверяется.** По умолчанию `validate_assignment` выключен, поэтому
  ограничение `le=70` при присваивании не срабатывает, и в ответе может оказаться возраст
  вне заявленного диапазона.
* **`str_min_length=3` не распространяется на `Address`.** Это настройка `model_config`
  модели `User`, а вложенная модель имеет собственную конфигурацию — поэтому `city='NY'`
  (2 символа) проходит.
* Закомментированный валидатор `check_name` (требование `istitle()`) несовместим с
  `str_to_upper=True`: `"JOHN".istitle()` → `False`.
* `ValidationError`/`HttpUrl` в `models.py` нужны только `Product` и блоку демонстрации.
  Неиспользуемый `List` из `typing` удалён.
