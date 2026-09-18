# -*- coding: utf-8 -*-
"""Запускаемые примеры к справочнику Pydantic v2.

    cd info/pydantic
    python examples.py

Каждый раздел печатает результат, в том числе для ошибок: ловушки показаны
не описанием, а настоящим исключением.
"""
import json
from datetime import date, datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    TypeAdapter,
    ValidationError,
    computed_field,
    field_validator,
    model_validator,
)


def title(n: int, text: str) -> None:
    print(f"\n{'=' * 70}\n{n}. {text}\n{'=' * 70}")


# ---------------------------------------------------------------------------
title(1, "BaseModel: вложенные модели и приведение типов")


class Address(BaseModel):
    city: str
    street: str
    house_number: str


class User(BaseModel):
    id: int
    name: str
    age: int
    is_active: bool = True
    address: Address


raw = {
    "id": "1",            # строка -> int
    "name": "John",
    "age": 22.0,          # float без дробной части -> int
    "is_active": 0,       # int -> bool
    "address": {"city": "NY", "street": "Main", "house_number": "10"},
}
user = User.model_validate(raw)
print("на входе было:", {k: type(v).__name__ for k, v in raw.items()})
print("стало        :", f"id={user.id!r} age={user.age!r} is_active={user.is_active!r}")
print("вложенная модель собралась сама:", type(user.address).__name__, user.address.city)

print("\nstrict=True запрещает такие приведения:")
try:
    User.model_validate(raw, strict=True)
except ValidationError as e:
    print("  ошибок:", e.error_count(), "| первая:", e.errors()[0]["msg"])

# ---------------------------------------------------------------------------
title(2, "Field и Annotated: ограничения вместо россыпи if")

positive_number = Annotated[float, Field(gt=0)]   # правило описано один раз


class Product(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50)]
    price: positive_number
    url: HttpUrl


p = Product(name="Чайник", price=19.99, url="https://example.com/item?id=1")
print("ок:", p.name, p.price, "| host:", p.url.host, "| scheme:", p.url.scheme)

for bad in ({"name": "Ча", "price": 10, "url": "https://e.com"},
            {"name": "Чайник", "price": -5, "url": "https://e.com"},
            {"name": "Чайник", "price": 10, "url": "не-ссылка"}):
    try:
        Product(**bad)
    except ValidationError as e:
        err = e.errors(include_url=False)[0]
        print(f"  {str(err['loc']):12} -> {err['msg']}")

# ---------------------------------------------------------------------------
title(3, "default против default_factory — ловушка общего значения")


class WrongId(BaseModel):
    id: UUID = uuid4()                       # ТАК НЕЛЬЗЯ: вычислится один раз


class RightId(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # вызовется для каждого объекта


print("default=uuid4()         :", WrongId().id == WrongId().id, "<- одинаковые у всех объектов")
print("default_factory=uuid4   :", RightId().id == RightId().id, "<- у каждого свой")

# ---------------------------------------------------------------------------
title(4, "ConfigDict: настройки всей модели")


class Tidy(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_to_upper=True, str_min_length=3)
    name: str
    address: Address          # вложенная модель живёт по СВОИМ правилам


t = Tidy(name="   John   ", address=Address(city="NY", street="Main", house_number="10"))
print(f"name: {'   John   '!r} -> {t.name!r}   (пробелы срезаны, регистр поднят)")
print(f"вложенная city={t.address.city!r} — 2 символа прошли, хотя str_min_length=3:")
print("  -> настройки model_config НЕ распространяются на вложенные модели")

print("\nextra='forbid' ловит опечатки в именах полей:")


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


try:
    Strict(nmae="John")
except ValidationError as e:
    for err in e.errors(include_url=False):
        print(f"  {str(err['loc']):10} -> {err['msg']}")

print("\nvalidate_assignment: проверять ли изменение уже созданного объекта")


class Loose(BaseModel):
    age: int = Field(ge=18, le=70)


class Tight(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    age: int = Field(ge=18, le=70)


loose = Loose(age=20)
loose.age += 999
print("  без validate_assignment: age =", loose.age, "<- ограничение le=70 не сработало")
try:
    tight = Tight(age=20)
    tight.age += 999
except ValidationError as e:
    print("  с validate_assignment  :", e.errors(include_url=False)[0]["msg"])

# ---------------------------------------------------------------------------
title(5, "field_validator: ЛОВУШКА с отступом")


class BrokenAppointment(BaseModel):
    """Валидатор объявлен ВНЕ тела класса — ровно так было в l06_practice."""
    appointment_date: datetime


# Этот декоратор стоит на уровне модуля, а не в классе выше:
@field_validator("appointment_date")
def never_called(cls, value):
    raise ValueError("сюда управление не попадёт")


class FixedAppointment(BaseModel):
    appointment_date: datetime

    @field_validator("appointment_date")
    @classmethod
    def check_date(cls, value: datetime):
        now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
        if value < now:
            raise ValueError("Дата и время приема должны быть в будущем")
        return value           # без этой строки в поле окажется None


past = datetime.now() - timedelta(days=1)
print("сломанная модель приняла дату в прошлом:", BrokenAppointment(appointment_date=past).appointment_date)
print("  -> Pydantic собирает валидаторы ТОЛЬКО из тела класса. Ошибки не было.")
try:
    FixedAppointment(appointment_date=past)
except ValidationError as e:
    print("исправленная модель:", e.errors(include_url=False)[0]["msg"])
print("будущая дата проходит:", FixedAppointment(appointment_date=datetime.now() + timedelta(days=3)).appointment_date.date())

print("\nВторая ловушка того же задания — валидатор без return:")


class NoReturn(BaseModel):
    value: int

    @field_validator("value")
    @classmethod
    def check(cls, v):
        if v < 0:
            raise ValueError("отрицательное")
        # return v забыли


print("  NoReturn(value=5).value =", NoReturn(value=5).value, "<- поле обнулилось, ошибки нет")

print("\nТретья ловушка — naive против aware:")
aware = datetime.now(timezone.utc) + timedelta(days=1)
try:
    naive_now = datetime.now()
    _ = aware < naive_now
except TypeError as e:
    print("  сравнение напрямую:", e)
print("  правильно: datetime.now(value.tzinfo) ->", FixedAppointment(appointment_date=aware).appointment_date.tzinfo)

# ---------------------------------------------------------------------------
title(6, "model_validator: проверка нескольких полей сразу")


class Employee(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    first_name: str
    last_name: str

    @model_validator(mode="after")
    def names_differ(self):
        if self.first_name.lower() == self.last_name.lower():
            raise ValueError("first_name and last_name must not be the same")
        return self            # без return self модель станет None


print("ок:", Employee(first_name="Elena", last_name="Petrova").first_name)
try:
    Employee(first_name="Ivan", last_name="ivan")
except ValidationError as e:
    print("поймано:", e.errors(include_url=False)[0]["msg"])

# ---------------------------------------------------------------------------
title(7, "computed_field: значение считается, но не хранится")


class Worker(BaseModel):
    hire_date: date
    salary: float

    @computed_field                # порядок важен: computed_field СВЕРХУ
    @property
    def years_worked(self) -> int:
        today = date.today()
        return today.year - self.hire_date.year - (
            (today.month, today.day) < (self.hire_date.month, self.hire_date.day)
        )

    @computed_field
    @property
    def actual_salary(self) -> float:
        bonus = 0.0 if self.years_worked < 3 else 0.10 if self.years_worked < 5 else 0.20
        return round(self.salary * (1 + bonus), 2)


w = Worker(hire_date=date(2015, 2, 1), salary=7000)
print("поля модели      :", list(Worker.model_fields))
print("в model_dump()   :", list(w.model_dump()))
print("  -> вычисляемые поля есть в выводе, но их нет среди хранимых полей")
print("значения         :", w.years_worked, "лет ->", w.actual_salary)
print("для файла их убираем:", w.model_dump(mode="json", exclude={"years_worked", "actual_salary"}))

# ---------------------------------------------------------------------------
title(8, "TypeAdapter: валидация списка, который не является моделью")

EmployeeListAdapter = TypeAdapter(list[Worker])     # создаём ОДИН раз

workers = EmployeeListAdapter.validate_python([
    {"hire_date": "2012-06-01", "salary": 80000},
    {"hire_date": "2024-01-10", "salary": 3000},
])
print("разобрано объектов:", len(workers))
print("dump_json возвращает", type(EmployeeListAdapter.dump_json(workers)).__name__, "-> нужен .decode()")
print(EmployeeListAdapter.dump_json(workers, indent=2).decode()[:170], "...")

print("\nу обычного списка методов модели нет:")
print("  hasattr(list, 'model_dump') ->", hasattr(list, "model_dump"))

# ---------------------------------------------------------------------------
title(9, "ValidationError.errors(): почему jsonify падал дважды")


class Mail(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def only_known_domains(cls, value):
        if value.split("@")[1] not in ("gmail.com", "yahoo.com"):
            raise ValueError("Invalid email address")
        return value


print("корректный адрес проходит:", Mail(email="john.doe@gmail.com").email)

try:
    Mail(email="john.doe@example.com")
except ValidationError as e:
    print("\nОшибка 1 — errors без скобок, это МЕТОД, а не свойство:")
    try:
        json.dumps(e.errors)
    except TypeError as te:
        print("   ", te)

    print("\nОшибка 2 — errors() со скобками, но с ctx по умолчанию:")
    try:
        json.dumps(e.errors())
    except TypeError as te:
        print("   ", te)
    print("    в ctx лежит:", repr(e.errors()[0].get("ctx", {}).get("error")))

    print("\nРабочий вариант — include_context=False:")
    ok = e.errors(include_url=False, include_context=False)
    print("   ", json.dumps(ok, ensure_ascii=False))

# ---------------------------------------------------------------------------
title(10, "model_dump: mode='python' против mode='json'")

print("mode='python':", w.model_dump(exclude={"years_worked", "actual_salary"}))
print("  типы        :", {k: type(v).__name__ for k, v in w.model_dump(exclude={"years_worked", "actual_salary"}).items()})
try:
    json.dumps(w.model_dump(exclude={"years_worked", "actual_salary"}))
except TypeError as e:
    print("  json.dumps  :", e, "<- date остался объектом")
print("mode='json'  :", w.model_dump(mode="json", exclude={"years_worked", "actual_salary"}))
print("  json.dumps  : работает")

print("\nexclude_unset — только то, что клиент реально прислал:")
partial = Worker.model_validate({"hire_date": "2020-01-01", "salary": 100})
print("  всё         :", list(partial.model_dump(exclude={'years_worked', 'actual_salary'})))
print("  exclude_unset:", list(partial.model_dump(exclude_unset=True, exclude={'years_worked', 'actual_salary'})))

print("\nГотово.")
