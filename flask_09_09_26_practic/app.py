from typing import Literal

from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict
from datetime import datetime, timedelta

from sqlalchemy import DECIMAL


class Event(BaseModel):
    """Задание 1
    Создайте модель Event, которая включает поля:
    ● title (строка),
    ● date (дата и время события),
    ● location (строка).
    Добавьте валидацию, чтобы дата события не была в прошлом.
    """

    title: str
    date: datetime
    location: str

    @field_validator('date')
    @classmethod
    def check_date(cls, value):
        if value < datetime.now():
            raise ValueError("Дата события не может быть в прошлом.")
        return value

try:
    future_event = Event(title="Future Event", date=datetime.now() + timedelta(days=30), location="New York")
    print(future_event)
except ValueError as e:
    print(f"ValidationError: {e}")


class UserProfiles(BaseModel):
    """ Задание 2
    Определите модель UserProfile с полями:
    ● username (строка),
    ● password (строка),
    ● email (строка с валидацией email).
    Используйте Field для добавления описаний и настройки валидации пароля (должен быть не менее 8
    символов)."""
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=2)
    username: str
    password: str = Field(..., min_length=8, description="Пароль должен быть не менее 8 символов.")
    email: EmailStr

    # class ConfigDict:
    #     str_strip_whitespace = True
    #     str_min_length = 3

# user_profile = UserProfiles(username="user", password="12345", email="user@example.com")
user_profile2 = UserProfiles(username="user2", password="12345678", email="user@example.com")
print(user_profile2)

class Transaction(BaseModel):
    """Задание 3
    Создайте модель Transaction с полями:
    ● amount (число),
    ● currency (строка, ограниченная до 3 символов),
    ● transaction_type (строка, принимает значения "debit" или "credit"),
    ● timestamp (дата и время).
    Добавьте валидацию, чтобы сумма транзакции была положительной."""

    amount: float = Field(gt=0, description="Сумма транзакции должна быть положительной.") # decimal.Decimal
    currency: str = Field(max_length=3, description="Код валюты должен быть не более 3 символов.")
    transaction_type: Literal['debit', 'credit'] = Field(description="Тип транзакции должен быть 'debit' или 'credit'.")
    timestamp: datetime

transaction = Transaction(amount=100.50, currency="USD", transaction_type="credit", timestamp=datetime.now())
print(transaction)


class Appointment(BaseModel):
    """Задание 4
    Определите модель Appointment с полями:
    ● appointment_date (дата и время приема),
    ● patient_name (строка),
    ● doctor_name (строка).
    Добавьте валидацию, чтобы дата и время приема были в будущем (не раньше текущей даты и времени)."""

    appointment_date: datetime
    patient_name: str
    doctor_name: str

@field_validator('appointment_date')

def appointment_date_validator(cls, value: datetime):
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
    min_allowed = now + timedelta(hours=24)

    if value < min_allowed:
        raise ValueError('Дата и время приема должны быть в будущем')

