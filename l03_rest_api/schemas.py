# Модели Pydantic (DTO)
# DTO (Data Transfer Object) — объект, описывающий ФОРМУ данных на границе приложения:
# что принимаем от клиента и что отдаём обратно. Бизнес-логика живёт в utils.py.

# date — тип «дата без времени» (для hire_date).
from datetime import date

# Annotated — «тип + метаданные», основной способ навесить Field(...) в Pydantic v2.
from typing import Annotated

# UUID  — тип идентификатора; uuid4 — генератор случайного UUID.
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,        # базовый класс модели
    ConfigDict,       # настройки поведения модели
    EmailStr,         # валидация email
    Field,            # ограничения и описания полей
    TypeAdapter,      # валидация/сериализация типов, не являющихся BaseModel (напр. list[Employee])
    computed_field,   # свойство, попадающее в сериализованный вывод
    model_validator,  # валидатор уровня модели (видит сразу все поля)
)

# Чистые функции расчёта вынесены в utils.py, чтобы модель не содержала бизнес-логику.
from .utils import calc_bonus_percent, calc_years_worked

# Вложенная модель адреса — используется как тип поля Employee.address.
class Address(BaseModel):
    city: str
    street: str
    house_number: str


# Основная модель сотрудника.
class Employee(BaseModel):
    # Обрезаем пробелы по краям у всех строковых полей модели.
    model_config = ConfigDict(str_strip_whitespace=True)

    # id не приходит от клиента — генерируется автоматически при создании объекта.
    # default_factory=uuid4 вызывается КАЖДЫЙ раз заново, поэтому у каждого сотрудника будет свой уникальный id
    # (в отличие от default=..., который вычислился бы один раз при объявлении класса)
    id: UUID = Field(default_factory=uuid4)

    # min_length/max_length — ограничения длины строки на уровне отдельного поля.
    first_name: Annotated[str, Field(min_length=2, max_length=50, description="First name")]
    last_name: Annotated[str, Field(min_length=2, max_length=50, description="Last name")]

    # Проверка формата почты (требует установленного пакета email-validator).
    email: EmailStr

    # Строка "2020-01-15" из JSON будет автоматически преобразована в объект date.
    hire_date: date

    # gt=0 — строго больше нуля; отрицательная и нулевая зарплата отвергаются.
    salary: Annotated[float, Field(gt=0, description="Base salary, before bonus")]

    # Вложенный объект: dict из JSON превратится в экземпляр Address.
    address: Address

    # спрашивали на занятии как проверить несколько полей сразу
    # mode="after" — валидатор срабатывает ПОСЛЕ проверки всех отдельных полей,
    # поэтому здесь self уже полностью собран и типы гарантированно корректны.
    @model_validator(mode="after")
    def check_names_are_different(self):
        # Сравниваем без учёта регистра: "Ivan"/"ivan" считаются одинаковыми.
        if self.first_name.lower() == self.last_name.lower():
            raise ValueError("first_name and last_name must not be the same")
        # Валидатор с mode="after" обязан вернуть сам объект модели.
        return self

    # вычисляемое поле, в файле (БД) не храним
    # @computed_field включает это свойство в model_dump()/model_dump_json(),
    # хотя оно не является настоящим полем модели.
    # Порядок декораторов важен: @computed_field идёт НАД @property.
    @computed_field
    @property
    def years_worked(self) -> int:
        # Стаж пересчитывается при каждом обращении — всегда актуален на сегодня.
        return calc_years_worked(self.hire_date)

    # вычисляемое поле, в файле (БД) не храним
    @computed_field
    @property
    def actual_salary(self) -> float:
        # Процент надбавки зависит от стажа (см. calc_bonus_percent).
        bonus = calc_bonus_percent(self.years_worked)
        # round(..., 2) — округление до копеек/центов.
        return round(self.salary * (1 + bonus), 2)


# Ошибки в Response клиент должен получать в унифицированном виде
class ErrorResponse(BaseModel):
    # Короткое название ошибки, например "Validation error".
    error: str
    # Подробности от Pydantic (результат e.errors()).
    # ОСТОРОЖНО: изменяемый объект [] как значение по умолчанию безопасен только
    # потому, что Pydantic делает для каждого экземпляра собственную копию
    # (в обычном классе Python это была бы классическая ошибка с общим списком).
    details: list = []


# Для валидации/сериализации списка моделей.
# Список — это не BaseModel и у него нет своих model_validate/model_dump, поэтому нужен TypeAdapter
# Создаётся один раз на уровне модуля: TypeAdapter кэширует скомпилированную схему.
EmployeeListAdapter = TypeAdapter(list[Employee])
