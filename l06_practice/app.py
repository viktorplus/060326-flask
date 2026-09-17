# Практика 09.09.26: четыре учебных задания на модели Pydantic.
# Каждый класс = отдельное задание, условие вынесено в docstring класса.

# Literal — тип «одно из перечисленных значений» (см. Transaction.transaction_type).
from typing import Literal

# field_validator — своя проверка конкретного поля.
# Field — ограничения и описания. EmailStr — валидация почты. ConfigDict — настройки модели.
from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict

# datetime — дата+время; timedelta — интервал (для сдвига «на 30 дней вперёд»).
from datetime import datetime, timedelta


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
        # ЧАСТАЯ ОШИБКА: сравнить пришедшую дату с голым datetime.now().
        # now() без аргумента возвращает «наивное» время (без часового пояса), и если
        # клиент пришлёт дату с поясом ("2026-10-01T12:00:00+02:00"), сравнение упадёт с
        # "TypeError: can't compare offset-naive and offset-aware datetimes". Так НЕ надо:
        # if value < datetime.now():

        # Правильно: берём «сейчас» в том же поясе, что и у пришедшего значения.
        # Если пояса нет — now() тоже будет наивным, и типы совпадут.
        now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
        if value < now:
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

    # ЧАСТАЯ ОШИБКА, из-за отступа. Раньше этот валидатор стоял на уровне МОДУЛЯ,
    # то есть вне тела класса. Pydantic собирает валидаторы только из тела класса,
    # поэтому проверка просто никогда не вызывалась: модель молча принимала любую
    # дату, в том числе прошедшую. Ни ошибки, ни предупреждения — самый неприятный
    # вид бага. Достаточно было сдвинуть декоратор и функцию на один уровень вправо.
    @field_validator('appointment_date')
    @classmethod
    def check_appointment_date(cls, value: datetime):
        # Тот же приём с часовым поясом, что и в задании 1.
        now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()

        if value < now:
            raise ValueError('Дата и время приема должны быть в будущем')

        # ВТОРАЯ ЧАСТАЯ ОШИБКА: забыть вернуть значение. Валидатор обязан отдать
        # value обратно — иначе Pydantic запишет в поле None, и модель «пройдёт»
        # проверку с пустой датой.
        return value


# Проверка задания 4: дата в прошлом должна быть отвергнута.
try:
    past_appointment = Appointment(
        appointment_date=datetime.now() - timedelta(days=1),
        patient_name='Ivan Petrov',
        doctor_name='Dr. House',
    )
    print(past_appointment)
except ValueError as e:
    print(f'ValidationError (ожидаемо, дата в прошлом): {e.errors()[0]["msg"]}')

# Проверка задания 4: корректная дата в будущем должна пройти и сохраниться.
future_appointment = Appointment(
    appointment_date=datetime.now() + timedelta(days=3),
    patient_name='Ivan Petrov',
    doctor_name='Dr. House',
)
print(future_appointment)
