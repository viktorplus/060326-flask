# Вспомогательный слой: чистые функции расчёта + чтение/запись «базы» в JSON-файл.

# Стандартный модуль работы с JSON.
import json

# Тип «дата без времени».
from datetime import date

# Путь к файлу-хранилищу вынесен в settings.py, чтобы не хардкодить его здесь.
from .settings import DATA_FILE


# Полное число отработанных лет на сегодняшний день.
def calc_years_worked(hire_date: date) -> int:
    # Текущая дата по локальному времени машины.
    today = date.today()
    # Разница по годам минус 1, если «годовщина» в этом году ещё не наступила.
    # Хитрость: сравнение кортежей (month, day) даёт True/False,
    # а bool в Python — подтип int, поэтому True вычитается как 1, False как 0.
    years = today.year - hire_date.year - ((today.month, today.day) < (hire_date.month, hire_date.day))
    return years


# Логика: стаж и надбавка за стаж
# 0-3 года -> +0%, 3-5 -> +10%, 5-10 -> +20%, 10+ -> +30%
def calc_bonus_percent(years: int) -> float:
    # Ранние return вместо elif-лесенки: каждая проверка отсекает свой диапазон,
    # поэтому нижняя граница уже гарантирована предыдущими условиями.
    if years < 3:
        return 0.0
    if years < 5:
        return 0.10
    if years < 10:
        return 0.20
    # Всё, что не отсеяно выше, — это 10 лет и больше.
    return 0.30


# Прочитать всех сотрудников из файла и вернуть список объектов Employee.
def load_employees() -> list:
    # Импорт ВНУТРИ функции, а не наверху файла, — чтобы разорвать циклический импорт:
    # schemas.py импортирует utils.py, а utils.py нуждается в schemas.Employee.
    from .schemas import Employee
    try:
        # encoding="utf-8" обязателен на Windows: иначе кодировка по умолчанию
        # (cp1251) сломает кириллицу в данных.
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            # json.load читает из файлового объекта (json.loads — из строки).
            raw_list = json.load(f)
    except FileNotFoundError:
        # Файла ещё нет (первый запуск) — это не ошибка, просто пустая «база».
        return []
    # Каждый словарь превращаем в валидированный объект Employee.
    # ** распаковывает ключи словаря в именованные аргументы модели.
    return [Employee(**item) for item in raw_list]


# Записать список сотрудников в файл, полностью перезаписав его.
def save_employees(employees: list) -> None:
    # years_worked/actual_salary исключаем из файла — это вычисляемые поля и их не нужно сохранять
    data = [
        # mode="json" превращает «непростые» типы (UUID, date) в строки,
        # иначе json.dump на них упадёт с TypeError.
        e.model_dump(mode="json", exclude={"years_worked", "actual_salary"})
        for e in employees
    ]
    # Режим "w" обнуляет файл — поэтому сюда всегда передаётся ПОЛНЫЙ список.
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # indent=4         — читаемое форматирование;
        # ensure_ascii=False — кириллица сохраняется как есть, а не как \uXXXX.
        json.dump(data, f, indent=4, ensure_ascii=False)
