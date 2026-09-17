# Практика 09.09.26: четыре учебных задания на модели Pydantic.
# Каждый класс = отдельное задание, условие вынесено в docstring класса.

# Literal — тип «одно из перечисленных значений» (см. Transaction.transaction_type).
from typing import Literal

# field_validator — своя проверка конкретного поля.
# Field — ограничения и описания. EmailStr — валидация почты. ConfigDict — настройки модели.
from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict

# datetime — дата+время; timedelta — интервал (для сдвига «на 30 дней вперёд»).
from datetime import datetime, timedelta

# Импорт из SQLAlchemy сделан «на будущее» (в комментарии у поля amount упомянут Decimal),
# в коде ниже DECIMAL не используется — этот импорт лишний.
from sqlalchemy import DECIMAL


class Event(BaseModel):
    """Задание 1
    Создайте модель Event, которая включает поля:
    ● title (строка),
    ● date (дата и время события),
    ● location (строка).
    Добавьте валидацию, чтобы дата события не была в прошлом.
    """

    # Три обязательных поля без значений по умолчанию.
    title: str
    date: datetime
    location: str

    # Валидатор привязан к полю 'date' и вызывается после приведения значения к datetime.
    @field_validator('date')
    # @classmethod ставится ПОД @field_validator; Pydantic добавил бы его и сам,
    # но явное указание даёт корректные подсказки типов в IDE.
    @classmethod
    def check_date(cls, value):
        # Сравниваем с текущим моментом. Тонкость: datetime.now() — «наивное» время
        # без часового пояса, поэтому сравнение с aware-датой вызвало бы TypeError.
        if value < datetime.now():
            # ValueError внутри валидатора Pydantic сам обернёт в ValidationError.
            raise ValueError("Дата события не может быть в прошлом.")
        # Валидатор обязан вернуть значение — иначе в поле окажется None.
        return value

# Проверка задания 1: дата на 30 дней вперёд — валидатор должен пропустить.
try:
    future_event = Event(title="Future Event", date=datetime.now() + timedelta(days=30), location="New York")
    print(future_event)
except ValueError as e:
    # ValidationError — наследник ValueError, поэтому этот except ловит и её тоже.
    print(f"ValidationError: {e}")


class UserProfiles(BaseModel):
    """ Задание 2
    Определите модель UserProfile с полями:
    ● username (строка),
    ● password (строка),
    ● email (строка с валидацией email).
    Используйте Field для добавления описаний и настройки валидации пароля (должен быть не менее 8
    символов)."""
    # Настройки для ВСЕХ строковых полей модели: обрезать пробелы, минимум 2 символа.
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=2)

    username: str

    # Ellipsis (...) первым аргументом Field означает «поле обязательное, значения по умолчанию нет».
    # min_length=8 на уровне поля строже, чем общий str_min_length=2 из model_config.
    password: str = Field(..., min_length=8, description="Пароль должен быть не менее 8 символов.")

    email: EmailStr

    # Неудачная попытка задать конфигурацию старым способом:
    # внутренний класс должен называться Config, а не ConfigDict,
    # поэтому такой блок был бы просто проигнорирован. Актуальный вариант — model_config выше.
    # class ConfigDict:
    #     str_strip_whitespace = True
    #     str_min_length = 3

# Эта строка падала бы с ValidationError: пароль "12345" короче 8 символов.
# user_profile = UserProfiles(username="user", password="12345", email="user@example.com")

# Корректный пример: пароль ровно 8 символов.
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
    # Ограничение "сумма положительна" задано прямо в Field(gt=0) — отдельный валидатор не нужен.

    # gt=0 — строго больше нуля. Комментарий про Decimal: для денег float неточен
    # (0.1 + 0.2 != 0.3), в реальных проектах берут decimal.Decimal.
    amount: float = Field(gt=0, description="Сумма транзакции должна быть положительной.") # decimal.Decimal

    # max_length=3 подходит для кодов ISO 4217: USD, EUR, RUB.
    currency: str = Field(max_length=3, description="Код валюты должен быть не более 3 символов.")

    # Literal сам по себе ограничивает набор допустимых значений — это и есть валидация;
    # Field здесь добавляет только описание.
    transaction_type: Literal['debit', 'credit'] = Field(description="Тип транзакции должен быть 'debit' или 'credit'.")

    timestamp: datetime

# Проверка задания 3: все ограничения соблюдены, объект создастся.
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

# ВНИМАНИЕ (незакрытое задание): валидатор ниже объявлен на уровне МОДУЛЯ,
# а не внутри класса Appointment — обратите внимание на отступ.
# Pydantic собирает валидаторы только из тела класса, поэтому эта проверка
# никогда не выполняется и модель принимает любую дату.
# Чтобы задание заработало, декоратор и функцию нужно сдвинуть на один уровень
# отступа внутрь класса Appointment.
@field_validator('appointment_date')

def appointment_date_validator(cls, value: datetime):
    # Если пришла дата с часовым поясом (tzinfo), берём «сейчас» в том же поясе,
    # иначе — наивное локальное время. Так избегаем TypeError при сравнении.
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()

    # Условие строже, чем в задании: запись должна быть минимум за 24 часа.
    min_allowed = now + timedelta(hours=24)

    if value < min_allowed:
        raise ValueError('Дата и время приема должны быть в будущем')
