
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict


class Event(BaseModel):

    title: str
    date:  datetime
    location: str

    @field_validator('date')
    @classmethod
    def date_validator(cls, v):
        if v < datetime.now():
            raise ValueError('Date must be in the future')
        return v

try:
    past_event = Event(
        title="Past Event",
        date=datetime.now() - timedelta(days=5),
        location="Past Location"
    )
    print(past_event)
except ValueError as e:
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
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=2, str_max_length=100)
    patern_name: str = Field(
        description='имя пациента должно быть строкой'
    )
    appointment_date: datetime = Field(
        description='дата и время приема должны быть в будущем'
    )

    @field_validator('appointment_date')
    @classmethod
    def appointment_date_validator(cls, v: datetime):
        now = datetime.now(v.tzinfo) if v.tzinfo else datetime.now() # Получаем текущее время с учетом часового пояса
        min_allower = now + timedelta(hours=24) # Минимальное допустимое время приема через 24 часа
        if v < min_allower:
            raise ValueError('Дата и время приема должны быть в будущем')
        return v


appt = Appointment(patern_name="John Doe", appointment_date=datetime.now() + timedelta(days=1, hours=1))
print(appt)

try:
    Appointment(patern_name="Jane Doe", appointment_date=datetime.now() + timedelta(hours=5))
except ValueError as e:
    print(f"Ошибка: {e}")
