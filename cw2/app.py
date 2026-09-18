from typing import Annotated, cast
import json
from datetime import datetime, date
from flask import (Flask, # импортируем Flask для создания веб-приложения
                   request, # импортируем request для получения данных из запроса
                   Response) # импортируем Response для формирования ответа на запрос
from pydantic import (
    BaseModel, # базовая модель Pydantic
    ValidationError, # исключение валидации
    ConfigDict, # конфигурация модели
    Field, # описание полей модели
    EmailStr, # тип для проверки email
    field_validator, # валидатор полей модели
    computed_field, # вычисляемое поле модели
    TypeAdapter # адаптер типов
)

class Address(BaseModel):
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


FILE_NAME = 'employees.json'

def save_employee(file_name: str, employee: Employee):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f) # загружаем данные из файла
    except (FileNotFoundError, json.JSONDecodeError):
        data = [] # если файла нет или он пустой, создаем пустой список
    data.append(employee.model_dump(mode='json')) # добавляем нового сотрудника в список
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f) # сохраняем список сотрудников в файл




app = Flask(__name__)
@app.route('/employee', methods=['POST'])
def employee_view():
    data = request.get_json() # получаем данные из запроса в виде словаря
    try:
        # employee = Employee.model_validate_json(request.data) # для string
        employee = Employee(**data) # для dict
        save_employee(FILE_NAME, employee) # сохраняем сотрудника в файл
        return Response(employee.model_dump_json(indent=4), mimetype='application/json', status=201)
    except ValidationError as e:
        return Response(json.dumps(e.errors()), status=400, mimetype='application/json')

@app.route('/employee/list', methods=['POST'])
def list_employee_view():
    pass

if __name__ == '__main__':
    app.run(debug=True)
