# Урок 03.09.26: модели Pydantic v2 — типы, Field, ConfigDict, валидаторы, наследование.

# Annotated — способ «приклеить» метаданные к типу: Annotated[тип, метаданные].
# List — устаревший аналог встроенного list[...] (оставлен из импорта, ниже не используется).
from typing import Annotated, List

# BaseModel      — базовый класс всех моделей.
# EmailStr       — тип-валидатор корректного email (требует пакет email-validator).
# ValidationError— исключение при неуспешной валидации.
# Field          — описание ограничений поля (gt, min_length, default и т.д.).
# HttpUrl        — тип-валидатор http/https-ссылки.
# field_validator— декоратор для собственной проверки конкретного поля.
# ConfigDict     — актуальный способ задать настройки модели.
from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDict


# Переиспользуемый "типизированный фрагмент" через Annotated:
# любое поле с типом positive_number будет float и обязано быть > 0 (gt=0).
# Удобно, когда одно и то же правило валидации нужно в нескольких моделях —
# не приходится дублировать Field(gt=0) в каждой модели отдельно.
positive_number = Annotated[float, Field(gt=0)]


# Модель товара — демонстрация разных способов описать поле.
class Product(BaseModel):
    # Простое обязательное поле: тип есть, значения по умолчанию нет.
    name: str

    # Необязательное поле: str | None + default=None.
    # description=... попадает в JSON Schema (документацию), на валидацию не влияет.
    description: Annotated[str | None, Field(default=None, description='Description of product')]

    # Используем заранее описанный тип positive_number — цена всегда > 0
    price: positive_number

    # Два способа задать значение по умолчанию сосуществуют:
    # здесь Field(...) несёт только описание, а сам default задан через "= False".
    in_stock: Annotated[bool, Field(description='Whether product is in stock')] = False

    # Список строк: Pydantic проверит и сам список, и каждый его элемент.
    tags: list[str]

    # HttpUrl отвергнет строку, которая не является корректным http(s)-адресом.
    url: HttpUrl


# Минимальная модель — показывает, что positive_number переиспользуется как обычный тип.
class Order(BaseModel):
    total: positive_number


# Вложенная модель: используется как тип поля внутри User (см. ниже).
class Address(BaseModel):
    house_number: str
    street: str
    city: str


# Основная учебная модель.
class User(BaseModel):
    # Конфигурация модели через актуальный (не deprecated) способ —
    # ConfigDict вместо старого внутреннего класса Config
    model_config = ConfigDict(
        str_strip_whitespace=True,   # обрезает пробелы по краям строк ("  John  " -> "John")
        str_to_upper=True,           # переводит ВСЕ строковые поля модели в верхний регистр
        str_min_length=3             # минимальная длина для всех строковых полей — 3 символа
    )

    # Обязательное целое поле.
    id: int

    # min_length/max_length работают на уровне ОТДЕЛЬНОГО поля и здесь
    # дублируют/уточняют общий str_min_length=3 из model_config
    name: Annotated[str, Field(min_length=3, max_length=50, description='Name of user')]

    # ge / le — «больше или равно» / «меньше или равно»: возраст в диапазоне [18, 70].
    age: Annotated[int, Field(ge=18, le=70, description='Age of user')]

    # EmailStr проверяет формат адреса; ниже к нему добавлен ещё и свой валидатор домена.
    email: Annotated[EmailStr, Field(description='Email of user')]

    # Поле со значением по умолчанию — в исходных данных его может не быть.
    is_active: bool = True

    # Вложенная модель: Pydantic сам превратит вложенный dict/JSON-объект в объект Address.
    address: Address

    # --- Старый (deprecated) способ конфигурации оставлен закомментированным
    # --- для сравнения с актуальным model_config выше. В реальном коде
    # --- использовать не нужно.
    # class Config:
    #     str_strip_whitespace = True
    #     str_min_length = 3

    # Ещё один закомментированный пример валидатора: требовать имя с заглавной буквы.
    # Не работает вместе со str_to_upper=True, потому что "JOHN".istitle() -> False.
    # @field_validator('name')
    # def check_name(cls, value):
    #     if value.istitle():
    #         return value
    #     raise ValueError('Name must be in title notation')

    # Кастомный валидатор для email: разрешены только домены gmail.com и yahoo.com.
    # Декоратор @field_validator('email') говорит Pydantic вызвать этот метод
    # ПОСЛЕ того, как значение прошло базовую проверку типа EmailStr.
    @field_validator('email')
    def check_email(cls, value):
        # Белый список допустимых доменов.
        allowed_domains = ['gmail.com', 'yahoo.com']

        _, domain = value.split('@')          # разделяем строку по @ на логин и домен
        if domain not in allowed_domains:
            raise ValueError('Invalid email address')  # именно ValueError, не ValidationError
        return value                            # обязательно вернуть значение обратно

    # Обычный метод модели — не имеет отношения к валидации,
    # просто пользовательская бизнес-логика
    def greetings(self):
        return f'Hello, {self.name}'

    # Переопределяем __str__, чтобы print(user) выводил только имя,
    # а не полное представление модели по умолчанию
    def __str__(self):
        return f'{self.name}'


# Наследование: Admin получает ВСЕ поля и методы User + добавляет своё поле
class Admin(User):
    # Дочерняя модель наследует и model_config, и валидатор check_email.
    is_admin: bool = True


# --- Создание объектов "вручную", через именованные аргументы ---

# Вложенный объект создаём отдельно и передаём его как готовый экземпляр.
# 'NY' короче str_min_length=3? Нет — ровно 2 символа, но ограничение задано
# в User.model_config и на модель Address не распространяется.
addr_1 = Address(city='NY', street='San Francisco', house_number='10')

# Пробелы вокруг 'John' срежет str_strip_whitespace, а str_to_upper сделает 'JOHN'.
user_1 = User(id=1, name='     John    ', age=20, is_active=True, address=addr_1, email='example@gmail.com')

# Благодаря переопределённому __str__ напечатается только имя.
print(user_1)


# --- Создание объекта из "внешних" данных, например пришедших по API ---

# Строка JSON — имитация тела запроса.
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

try:
    # Разбор строки JSON + валидация одним вызовом.
    # strict=False разрешает 22.0 -> 22 (float в int) и 0 -> False (int в bool).
    user = User.model_validate_json(json_string, strict=False)
    print(user)

    # Присваивание без повторной валидации (validate_assignment по умолчанию выключен).
    user.age += 10

    # Обратная сериализация модели в строку JSON с отступами.
    res = user.model_dump_json(indent=4)
    print(res)
except ValidationError as e:
    # Сюда попадём, например, если домен почты не из белого списка
    # или возраст вышел за границы [18, 70].
    print(f'ValidationError: {e}')
