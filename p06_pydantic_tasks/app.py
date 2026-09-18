# Практическая работа: четыре задания на модели Pydantic.
# Те же четыре задания решены в l06_practice — это второе, независимое решение.
# Оно местами удачнее: валидатор задания 4 сразу объявлен внутри класса,
# а для денег взят Decimal, а не float. Сравнение — в SCHEMA.md рядом.
#
# Запускать из каталога проекта:
#     cd p06_pydantic_tasks
#     python app.py

# datetime — дата и время; timedelta — интервал.
from datetime import datetime, timedelta
# Decimal — точное десятичное число. Для денег берут его, а не float:
# двоичная дробь не представляет 0.1 точно, и суммы «уезжают» на копейки.
from decimal import Decimal
# Literal — тип «одно из перечисленных значений».
from typing import Literal

from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict


class Event(BaseModel):
    """Задание 1. Модель Event: title, date, location.
    Валидация: дата события не может быть в прошлом."""

    title: str
    date:  datetime
    location: str

    @field_validator('date')
    @classmethod
    def date_validator(cls, v):
        # ЧАСТАЯ ОШИБКА: сравнить пришедшую дату с голым datetime.now().
        # now() без аргумента даёт «наивное» время, без часового пояса. Стоит клиенту
        # прислать дату с поясом ("2026-10-01T12:00:00+02:00") — и сравнение упадёт с
        # "TypeError: can't compare offset-naive and offset-aware datetimes".
        # Так НЕ надо:
        # if v < datetime.now():

        # Правильно: берём «сейчас» в том же поясе, что у пришедшего значения.
        # Пояса нет — now() тоже будет наивным, и типы совпадут.
        now = datetime.now(v.tzinfo) if v.tzinfo else datetime.now()
        if v < now:
            # ValueError внутри валидатора Pydantic сам завернёт в ValidationError.
            raise ValueError('Date must be in the future')
        # Валидатор обязан вернуть значение — иначе в поле окажется None.
        return v

# Проверка задания 1: дата в прошлом должна быть отвергнута.
try:
    past_event = Event(
        title="Past Event",
        date=datetime.now() - timedelta(days=5),
        location="Past Location"
    )
    print(past_event)
except ValueError as e:
    # ValidationError — наследник ValueError, поэтому этот except ловит и её.
    print(f"Ошибка: {e}")


class UserProfile(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=2, str_max_length=50)
    username: str = Field(
        description='имя пользователя должно быть от 2 до 50 символов'
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description='пароль должен быть от 8 до 100 символов'
    )
    email: EmailStr = Field(
        description='электронная почта должна быть действительным адресом электронной почты'
    )

user_profile = UserProfile(username="john_doe", password="securePassword123", email="john.doe@example.com")
print(user_profile)


class Transaction(BaseModel):
    amount: Decimal = Field(
        description='сумма транзакции должна быть положительным числом',
        gt=0
    )
    transaction_type: Literal['debit', 'credit'] = Field(
        description='тип транзакции должен быть либо "debit", либо "credit"'
    )
    currency: str = Field(
        description='валюта транзакции должна быть строкой из 3 символов',
        min_length=3,
        max_length=3
    )

    @field_validator('currency')
    @classmethod
    def currency_validator(cls, v: str):
        if not v.isalpha():
            raise ValueError('Currency должен быть только буквы')
        return v.upper()

tx = Transaction(amount=Decimal('100.50'), transaction_type='credit', currency='usd')
print(tx)

try:
    Transaction(amount=Decimal('-100.50'), transaction_type='credit', currency='usd')
except ValueError as e:
    print(f"Ошибка: {e}")

class Appointment(BaseModel):
    """Задание 4. Модель Appointment: appointment_date, patient_name, doctor_name.
    Валидация: дата и время приёма должны быть в будущем."""

    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=2, str_max_length=100)

    # Было `patern_name` — опечатка в слове patient. Имя поля это часть контракта:
    # клиент, присылающий корректное patient_name, получил бы «поле обязательно»
    # на patern_name и не понял бы, чего от него хотят.
    patient_name: str = Field(
        description='имя пациента должно быть строкой'
    )
    # Поля doctor_name в решении не было, хотя условие задания его требует.
    doctor_name: str = Field(
        description='имя врача должно быть строкой'
    )
    appointment_date: datetime = Field(
        description='дата и время приема должны быть в будущем'
    )

    @field_validator('appointment_date')
    @classmethod
    def appointment_date_validator(cls, v: datetime):
        # Тот же приём с часовым поясом, что и в задании 1.
        now = datetime.now(v.tzinfo) if v.tzinfo else datetime.now()

        # ЗАМЕЧАНИЕ. Условие задания требует всего лишь «не раньше текущего момента»,
        # а здесь правило строже: записаться можно минимум за 24 часа. Это осознанное
        # ужесточение — в жизни регистратуре нужен запас времени. Оставлено как есть,
        # но знать о расхождении с условием полезно: в l06_practice то же задание
        # решено буквально по тексту.
        min_allowed = now + timedelta(hours=24)  # было min_allower — опечатка
        if v < min_allowed:
            raise ValueError('Дата и время приема должны быть не раньше чем через 24 часа')
        return v


# Проверка задания 4: запись через 25 часов — проходит.
appt = Appointment(
    patient_name="John Doe",
    doctor_name="Dr. House",
    appointment_date=datetime.now() + timedelta(days=1, hours=1),
)
print(appt)

# А через 5 часов — нет: не хватает суточного запаса.
try:
    Appointment(
        patient_name="Jane Doe",
        doctor_name="Dr. House",
        appointment_date=datetime.now() + timedelta(hours=5),
    )
except ValueError as e:
    print(f"Ошибка: {e}")
