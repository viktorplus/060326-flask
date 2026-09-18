from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDict
from typing import Annotated, List


positive_number = Annotated[float, Field(gt=0)]

class Product(BaseModel):
    name: str
    description: Annotated[
        str,
        Field(default=None, description="Description of product")
    ]

    price: positive_number

    in_stock: Annotated[
        bool,
        Field(default=False, description="Whether product is in stock")] = False

    tags: list[str]
    url: HttpUrl

"""
#!!! вариант написания без Annotations
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    description: str | None = Field(
        default=None,
        description="Description of product"
    )
    price: float = Field(
        gt=0,
        description="Price of product"
    )
    in_stock: bool = Field(
        default=False,
        description="Whether product is in stock"
    )"""




class Order(BaseModel):
    total:positive_number

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

    name: Annotated[str, Field(min_length=3, max_length=50, description="User's name")]

    age: Annotated[int, Field(ge=18, le=70, description="User's age")]
    email: EmailStr
    is_active: bool = True
    address: Address

    # class Config:
    #     str_strip_whitespace = True
    #     str_min_length = 3


@field_validator("email")
def check_email(cls, value: str) -> str:
    allowed_domains = ["gmail.com", "yahoo.com"]
    _, domain = value.split("@")
    if domain not in allowed_domains:
        raise ValueError(f"Email domain '{domain}' is not allowed. Allowed domains: {allowed_domains}")
    return value


# @field_validator("name")
# def check_name(cls, value: str) -> str:
#     if value.istitle():
#         return value
#     raise ValueError("Name must be capitalized")





def greetings(self) -> str:
        return (
            f"Hello {self.name}, welcome to the app!"
        )

# addr_1 = Address(city='NY', street='San Francisco', house_number='10')
# user_1 = User(id=1, name='John', age=20, is_active=True, address=addr_1, email='example@gmail.com')
# print(user_1)


# json_string = """{
#     "id": 1,
#     "name": "John Doe",
#     "age": 22.0,
#     "email": "john.doe@example.com",
#     "is_active": 0,
#     "address": {
#         "city": "New York",
#         "street": "5th Avenue",
#         "house_number": "123"
#     }
# }"""

# bool - int
# int - float

# try:
#     user = User.model_validate_json(json_string, strict=False)
#     print(user)
#     user.age += 10
#     res = user.model_dump_json(indent=4)
#     print(res)
# except ValidationError as e:
#     print(f'ValidationError: {e}')

