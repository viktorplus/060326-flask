# BaseModel

```python
from pydantic import BaseModel
```

**Что это.** Базовый класс всех моделей. Наследник описывает поля аннотациями типов, а Pydantic по ним строит валидацию и сериализацию.

**Зачем.** Данные извне (тело HTTP-запроса, JSON-файл, форма) приходят без гарантий. Модель — это контракт: либо на выходе корректный объект нужных типов, либо `ValidationError` с описанием, что именно не так. Проверять поля вручную через `if` долго и легко забыть случай.

## Сигнатура

```python
class MyModel(BaseModel):
    field_name: type = default

MyModel(**data)                  # из именованных аргументов
MyModel.model_validate(obj)      # из dict
MyModel.model_validate_json(s)   # из строки JSON
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| `model_config` | ConfigDict | `{}` | Настройки всей модели: обрезка пробелов, запрет лишних полей и т.д. |
| `model_fields` | dict | — | Служебный атрибут: описание всех полей модели |

## Минимальный пример

```python
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    street: str
    house_number: str

class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True         # значение по умолчанию -> поле необязательное
    address: Address               # вложенная модель

user = User(id=1, name='John', age=20,
            address=Address(city='NY', street='Main', house_number='10'))
print(user.name, user.address.city)
```

Вывод:

```
John NY
```

## Типичные задачи

**Вложенные модели собираются из вложенных словарей автоматически**

```python
data = {'id': 1, 'name': 'John', 'age': 20,
        'address': {'city': 'NY', 'street': 'Main', 'house_number': '10'}}
user = User(**data)          # Address создастся сам
```

**Наследование: дочерняя модель получает все поля и валидаторы родителя**

```python
class Admin(User):
    is_admin: bool = True
```

**Свои методы и __str__ — модель остаётся обычным классом**

```python
class User(BaseModel):
    name: str

    def greetings(self):
        return f'Hello, {self.name}'

    def __str__(self):
        return self.name
```

## Частые ошибки

- **Изменяемое значение по умолчанию.** `tags: list[str] = []` в обычном классе было бы ошибкой (один список на все экземпляры), но Pydantic делает копию для каждого объекта — здесь это безопасно. Не переносите привычку обратно в обычные классы.
- **Присваивание не валидируется.** `user.age = 999` пройдёт молча: по умолчанию `validate_assignment=False`. Включается через `model_config`.
- **Код верхнего уровня в модуле с моделями.** Если рядом с классами лежат вызовы и `print`, они выполнятся при каждом импорте. В этом репозитории из-за такого при старте сервера в консоль улетал пойманный `ValidationError`. Прячьте демонстрации в `if __name__ == '__main__':`.
- **Настройки `model_config` не наследуются вложенными моделями.** `str_min_length=3` у `User` не действует на `Address` — у неё своя конфигурация.

## Где в репозитории

- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:24` — `class Product(BaseModel):`
- `l02_pydantic_models/models.py:47` — `class Order(BaseModel):`
- `l02_pydantic_models/models.py:52` — `class Address(BaseModel):`

## См. также

[Field](Field.md), [ConfigDict](ConfigDict.md), [field_validator](field_validator.md), [model_validate](model_validate.md)
