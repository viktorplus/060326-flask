import os

from flask import Flask, Response, request
from pydantic import ValidationError
from dotenv import load_dotenv
from .schemas import Employee, EmployeeListAdapter, ErrorResponse
from .utils import load_employees, save_employees

load_dotenv()

DB_USERNAME = os.environ.get("DB_USERNAME")



app = Flask(__name__)


def error_response(e: ValidationError, status: int = 400) -> Response:
    # include_context=False — чтобы в ответе не оказалось несериализуемых
    # в JSON объектов (например, исходного исключения из валидатора)
    error = ErrorResponse(error="Validation error", details=e.errors(include_url=False, include_context=False))
    return Response(error.model_dump_json(indent=4), status=status, mimetype="application/json")

@app.route("/employees", methods=["GET", "POST"])
def employees_view():
    # POST - сохранить сотрудника к файл
    if request.method == "POST":
        try:
            employee = Employee(**request.get_json(force=True))
        except ValidationError as error:
            return error_response(error)

        # employee.id уже сгенерирован автоматически (default_factory=uuid4)
        employees = load_employees()
        employees.append(employee)
        save_employees(employees)

        return Response(employee.model_dump_json(indent=4), status=201, mimetype="application/json")

    # GET — вернуть всех сотрудников из файла
    employees = load_employees()
    return Response(EmployeeListAdapter.dump_json(employees, indent=4), status=200, mimetype="application/json")


@app.route("/employees/batch", methods=["POST"])
def employees_batch_view():
    try:
        new_employees = EmployeeListAdapter.validate_python(request.get_json(force=True))
    except ValidationError as exc:
        return error_response(exc)

    employees = load_employees()
    employees.extend(new_employees)
    save_employees(employees)

    return Response(EmployeeListAdapter.dump_json(new_employees, indent=4), status=201, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)