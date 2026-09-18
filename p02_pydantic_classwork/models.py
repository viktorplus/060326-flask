# Модели Pydantic к классной работе 03.09.
# Отличия от l02_pydantic_models/models.py отмечены по месту.

from typing import Annotated
from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDict


positive_number = Annotated[float, Field(gt=0)]


class Product(BaseModel):
    name: str
    description: Annotated[str, Field(default=None, description='Description of product')]
    price: positive_number
    in_stock: Annotated[bool, Field(description='Whether product is in stock')] = False
    tags: list[str]
    url: HttpUrl


class Order(BaseModel):
    total: positive_number

class Address(BaseModel):
    house_number: str
    street: str
    city: str


class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_upper=True,
        str_min_length=3
    )
    id: int
    name: Annotated[str, Field(min_length=3, max_length=50, description='Name of user')]
    age: Annotated[int, Field(ge=18, le=70, description='Age of user')]
    # ОТЛИЧИЕ от урока: здесь Field стоит справа от знака "=", а не внутри Annotated.
    # Оба варианта рабочие и дают одинаковый результат. Разница в том, что при записи
    # через Annotated значение по умолчанию остаётся справа от "=", а ограничения
    # живут в типе — и такой тип можно объявить один раз и переиспользовать.
    email: EmailStr = Field(description='Email of user')
    # email: Annotated[EmailStr, Field(description='Email of user')]   # так в уроке

    is_active: bool = True
    address: Address

    # class Config:
    #     str_strip_whitespace = True
    #     str_min_length = 3


    # @field_validator('name')
    # def check_name(cls, value):
    #     if value.istitle():
    #         return value
    #     raise ValidationError('Name must be in title notation')

    @field_validator('email')
    def check_email(cls, value):
        allowed_domains = ['gmail.com', 'yahoo.com']

        _, domain = value.split('@')
        if domain not in allowed_domains:
            raise ValueError('Invalid email address')
        return value


    def greetings(self):
        return f'Hello, {self.name}'

    def __str__(self):
        return f'{self.name}'


class Admin(User):
    is_admin: bool = True

# Демонстрация ниже закрыта защитой __name__ == '__main__'.
# ЗАЧЕМ. app.py делает `from models import User`, а импорт выполняет модуль целиком.
# Без защиты примеры отрабатывали бы при каждом старте сервера и печатали в консоль
# лишнее, в том числе пойманную ValidationError — легко принять за сбой приложения.
# Запустить примеры отдельно: python models.py
if __name__ == '__main__':
    addr_1 = Address(city='NY', street='San Francisco', house_number='10')
    user_1 = User(id=1, name='     John    ', age=20, is_active=True, address=addr_1, email='example@gmail.com')
    print(user_1)


    json_string = """{
        "id": 1,
        "name": "John Doe",
        "age": 22.0,
        "email": "john.doe@example.com",
        "is_active": 0,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": "123"
        }
    }"""

    # bool - int
    # int - float

    try:
        user = User.model_validate_json(json_string, strict=False)
        print(user)
        user.age += 10
        res = user.model_dump_json(indent=4)
        print(res)
    except ValidationError as e:
        print(f'ValidationError: {e}')

