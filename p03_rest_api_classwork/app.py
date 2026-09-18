# Классная работа к уроку 04.09: REST API «сотрудники» — но ОДНИМ файлом.
# Тот же урок разобран в l03_rest_api, где код разложен по слоям
# (app.py / schemas.py / utils.py / settings.py). Сравнение двух подходов —
# в SCHEMA.md рядом.
#
# Запускать из каталога проекта:
#     cd p03_rest_api_classwork
#     python app.py

from typing import Annotated
import json
from datetime import date

from flask import (Flask,     # импортируем Flask для создания веб-приложения
                   request,   # импортируем request для получения данных из запроса
                   Response)  # импортируем Response для формирования ответа на запрос
from pydantic import (
    BaseModel,        # базовая модель Pydantic
    ValidationError,  # исключение валидации
    ConfigDict,       # конфигурация модели
    Field,            # описание полей модели
    EmailStr,         # тип для проверки email
    TypeAdapter       # адаптер типов: нужен для валидации СПИСКА моделей
)


class Address(BaseModel):
    # extra='forbid' — не принимать поля, которых нет в модели.
    # Это строже, чем по умолчанию ('ignore'), и ловит опечатки в именах:
    # {'ctiy': 'NY'} даст понятную ошибку вместо молчаливой потери значения.
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True, str_min_length=1)
    street: Annotated[str, Field(max_length=100)]
    city: Annotated[str, Field(max_length=50)]
    house_number: Annotated[str, Field(max_length=50)]


class Employee(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True, str_min_length=1)
    first_name: Annotated[str, Field(max_length=50)]
    last_name: Annotated[str, Field(max_length=50)]
    email: EmailStr
    hire_date: date
    salary: Annotated[float, Field(gt=0)]
    address: Address


# Путь ОТНОСИТЕЛЬНЫЙ: разрешается от рабочего каталога процесса, а не от этого файла.
# Отсюда требование запускать проект из его каталога — иначе файл будет создан не там,
# и ошибки при этом не возникнет.
FILE_NAME = 'employees.json'

# Список моделей — это не BaseModel, у него нет model_validate/model_dump.
# TypeAdapter закрывает эту дыру. Создаём ОДИН раз на уровне модуля:
# адаптер компилирует схему, и пересоздавать его в каждом запросе дорого.
EmployeeListAdapter = TypeAdapter(list[Employee])


def load_employees(file_name: str) -> list[Employee]:
    """Читает файл-хранилище. Нет файла или он пустой — считаем, что список пуст."""
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return EmployeeListAdapter.validate_python(data)


def save_employee(file_name: str, employee: Employee):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)  # загружаем данные из файла
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # если файла нет или он пустой, создаем пустой список

    # mode='json' обязателен: без него hire_date останется объектом date,
    # и json.dump упадёт с "Object of type date is not JSON serializable".
    data.append(employee.model_dump(mode='json'))  # добавляем нового сотрудника в список

    with open(file_name, 'w', encoding='utf-8') as f:
        # ensure_ascii=False — чтобы кириллица в именах осталась читаемой,
        # а не превратилась в \uXXXX. indent=4 — чтобы файл можно было открыть глазами.
        json.dump(data, f, indent=4, ensure_ascii=False)


app = Flask(__name__)


@app.route('/employee', methods=['POST'])
def employee_view():
    # force=True — разбирать тело как JSON, даже если клиент забыл заголовок
    # Content-Type: application/json. Без него такой запрос отдаёт 415.
    data = request.get_json(force=True)  # получаем данные из запроса в виде словаря
    try:
        # employee = Employee.model_validate_json(request.data) # для string
        employee = Employee(**data)  # для dict
        save_employee(FILE_NAME, employee)  # сохраняем сотрудника в файл
        return Response(employee.model_dump_json(indent=4), mimetype='application/json', status=201)
    except ValidationError as e:
        # include_context=False здесь обязателен на будущее: как только в модели
        # появится свой field_validator, бросающий ValueError, этот объект попадёт
        # в ключ 'ctx' и json.dumps упадёт с
        # "Object of type ValueError is not JSON serializable".
        # Сейчас валидаторы только встроенные, и без флага тоже работает —
        # но ошибка вылезла бы позже и не там, где её ждут. Разбор: l02_pydantic_models.
        errors = e.errors(include_url=False, include_context=False)
        return Response(json.dumps(errors, ensure_ascii=False), status=400,
                        mimetype='application/json')


@app.route('/employee/list', methods=['GET'])
def list_employee_view():
    # Раньше тело этого обработчика было `pass`. Функция возвращала None,
    # и Flask отвечал 500 с "The view function ... did not return a valid response".
    # Маршрут выглядел рабочим, пока в него не постучишься.
    #
    # Заодно исправлен метод: было POST, а чтение списка — это GET.
    # POST означает «создай что-то», и на нём кешированию и повторам взяться неоткуда.
    employees = load_employees(FILE_NAME)
    return Response(EmployeeListAdapter.dump_json(employees, indent=4),
                    status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
