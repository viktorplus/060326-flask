## Общий сценарий POST-запроса

В полноценном обработчике логика выглядит так:

1. Клиент отправляет POST-запрос с JSON.
2. Сервер извлекает тело запроса.
3. Pydantic валидирует JSON и создаёт объект.
4. Приложение выполняет бизнес-логику и при необходимости работает с базой данных.
5. Результат сериализуется.
6. Сервер возвращает JSON-ответ с корректным `Content-Type`.

Упрощённый пример:

from flask import Flask, Response, request
from pydantic import ValidationError

app = Flask(__name__)


@app.post("/users")
def create_user():
    try:
        user = User.model_validate(request.get_json())
    except ValidationError as error:
        return Response(error.json(), status=400, mimetype="application/json")

    return Response(
        user.model_dump_json(),
        status=201,
        mimetype="application/json",
    )

Здесь для уже разобранного Flask-словаря применяется `model_validate()`.
Если на входе именно необработанная JSON-строка, используется `model_validate_json()`.

jsonify и готовая JSON-строка, удобно применять, когда исходные данные представлены словарём или списком Python:

from flask import jsonify

@app.get("/user")
def get_user():
    return jsonify({"id": 1, "name": "Alex"})

Если Pydantic уже вернул готовую JSON-строку через `model_dump_json()`,
повторно сериализовать её с помощью `jsonify()` не нужно.