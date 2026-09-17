# Урок 04.09.26: мини-REST API «сотрудники» — Flask + Pydantic + хранение в JSON-файле.
# Запускать как пакет из корня проекта: python -m l03_rest_api.app
# (относительные импорты ниже работают только при таком запуске).

# os — доступ к переменным окружения.
import os

# Flask   — приложение.
# Response— ручной объект ответа (тело + статус + mimetype).
# request — «магический» объект текущего HTTP-запроса (метод, заголовки, тело).
from flask import Flask, Response, request

# Исключение валидации Pydantic.
from pydantic import ValidationError

# Читает файл .env и кладёт его содержимое в переменные окружения процесса.
from dotenv import load_dotenv

# Относительные импорты внутри пакета (точка = «текущий пакет l03_rest_api»).
from .schemas import Employee, EmployeeListAdapter, ErrorResponse
from .utils import load_employees, save_employees

# Выполняем загрузку .env ДО чтения переменных ниже, иначе они окажутся None.
load_dotenv()

# Секреты берём только из окружения и никогда не хардкодим в исходнике.
DB_USERNAME = os.environ.get("DB_USERNAME")
DRIVER = os.environ.get("DRIVER")

# Заготовка строки подключения к БД (в этом уроке ещё не используется —
# данные лежат в JSON-файле, а не в базе).
conn_str = f'{DRIVER}'

# Экземпляр приложения.
app = Flask(__name__)


# Общий помощник: превращает ошибку валидации в единообразный JSON-ответ.
# Вынесен в функцию, чтобы не дублировать один и тот же код в каждом обработчике.
def error_response(e: ValidationError, status: int = 400) -> Response:
    # include_context=False — чтобы в ответе не оказалось несериализуемых
    # в JSON объектов (например, исходного исключения из валидатора)
    # include_url=False убирает ссылки на документацию pydantic из каждой ошибки.
    error = ErrorResponse(error="Validation error", details=e.errors(include_url=False, include_context=False))
    # 400 Bad Request по умолчанию — клиент прислал некорректные данные.
    return Response(error.model_dump_json(indent=4), status=status, mimetype="application/json")

# Один URL обслуживает два метода: список (GET) и создание (POST).
# Без methods=[...] Flask разрешил бы только GET.
@app.route("/employees", methods=["GET", "POST"])
def employees_view():
    # POST - сохранить сотрудника к файл
    if request.method == "POST":
        try:
            # get_json(force=True) разбирает тело как JSON, даже если клиент
            # не прислал заголовок Content-Type: application/json.
            # ** распаковывает полученный dict в именованные аргументы модели.
            employee = Employee(**request.get_json(force=True))
        except ValidationError as error:
            # Данные не прошли проверку — отдаём 400 и список ошибок.
            return error_response(error)

        # employee.id уже сгенерирован автоматически (default_factory=uuid4)

        # Читаем текущее содержимое файла (список объектов Employee).
        employees = load_employees()
        # Добавляем нового сотрудника в конец.
        employees.append(employee)
        # Перезаписываем файл целиком.
        # Примечание: это не атомарно и не потокобезопасно — для учебного примера нормально.
        save_employees(employees)

        # 201 Created — стандартный статус для успешного создания ресурса.
        # В теле возвращаем созданный объект (уже с id и вычисляемыми полями).
        return Response(employee.model_dump_json(indent=4), status=201, mimetype="application/json")

    # GET — вернуть всех сотрудников из файла
    employees = load_employees()
    # dump_json у TypeAdapter сериализует СПИСОК моделей — у списка нет своего model_dump_json.
    return Response(EmployeeListAdapter.dump_json(employees, indent=4), status=200, mimetype="application/json")


# Отдельный маршрут для пакетной загрузки: клиент присылает массив сотрудников сразу.
@app.route("/employees/batch", methods=["POST"])
def employees_batch_view():
    try:
        # validate_python проверяет уже разобранную Python-структуру (список dict'ов)
        # и возвращает список готовых объектов Employee.
        new_employees = EmployeeListAdapter.validate_python(request.get_json(force=True))
    except ValidationError as exc:
        # Если хотя бы один элемент списка невалиден — весь запрос отклоняется.
        return error_response(exc)

    # Дочитываем то, что уже лежит в файле...
    employees = load_employees()
    # ...и расширяем список новыми элементами (extend, а не append — добавляем список к списку).
    employees.extend(new_employees)
    save_employees(employees)

    # Возвращаем только добавленных сотрудников, а не весь файл.
    return Response(EmployeeListAdapter.dump_json(new_employees, indent=4), status=201, mimetype="application/json")


# Точка входа при прямом запуске файла.
if __name__ == "__main__":
    app.run(debug=True)
