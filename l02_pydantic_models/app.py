# Урок 03.09.26: связка Flask + Pydantic — валидация входного JSON и ручная отдача Response.

# Flask        — класс приложения.
# jsonify      — превращает dict/list в готовый Response с mimetype application/json.
# Response     — «ручной» объект ответа: сами задаём тело, статус и mimetype.
from flask import Flask, jsonify, Response

# ValidationError — исключение, которое Pydantic бросает, если данные не прошли проверку.
from pydantic import ValidationError

# Импорт модели User из соседнего файла models.py.
# ВАЖНО: импорт абсолютный (не `from .models import`), поэтому запускать нужно
# из каталога l02_pydantic_models, иначе Python не найдёт модуль.
# Побочный эффект: код на верхнем уровне models.py выполнится прямо при импорте.
from models import User

# Экземпляр приложения.
app = Flask(__name__)


# Главная страница: демонстрация разбора JSON-строки через Pydantic.
@app.route('/')
def index():
    # Тройные кавычки — многострочный литерал. Имитируем «данные, пришедшие извне».
    json_string = """{
        "id": 1,
        "name": "John Doe",
        "age": 22.0,
        "email": "john.doe@example.com",
        "is_active": 0,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": "123"
        }
    }"""

    # Заметки с занятия: в нестрогом режиме Pydantic делает «безопасные» приведения типов.
    # bool - int    -> 0/1 превращается в False/True (поле is_active)
    # int - float   -> 22.0 превращается в 22 (поле age)

    try:
        # model_validate_json: разбирает СТРОКУ JSON и сразу валидирует её по модели.
        # strict=False (значение по умолчанию) разрешает приведение типов, описанное выше.
        user = User.model_validate_json(json_string, strict=False)

        # Печатает в консоль сервера. У User переопределён __str__, поэтому увидим только имя.
        print(user)

        # Модели Pydantic по умолчанию изменяемые: можно присвоить новое значение полю.
        # ВНИМАНИЕ: при обычном присваивании валидация НЕ перезапускается
        # (для этого нужен ConfigDict(validate_assignment=True)),
        # поэтому ограничение le=70 здесь не проверяется.
        user.age += 10

        # model_dump_json — сериализация модели обратно в строку JSON.
        # indent=4 — «красивый» человекочитаемый вывод.
        res = user.model_dump_json(indent=4)

        # Отдаём готовую строку как JSON-ответ. jsonify здесь не подходит:
        # он ожидает dict/list, а у нас уже готовая строка.
        return Response(res, mimetype='application/json')
    except ValidationError as e:
        # Если данные не прошли валидацию — отдаём описание ошибок.
        # ОСТОРОЖНО (учебный баг): e.errors — это МЕТОД, а не свойство.
        # Без скобок сюда попадёт сам объект метода, и jsonify упадёт.
        # Правильно: jsonify(e.errors())
        return jsonify(e.errors)


# Дальше — те же учебные маршруты, что и в l01_routing/app.py.

# Статический маршрут.
@app.route('/menu')
def menu():
    return 'Menu of MyCafe'

# Динамический сегмент с конвертером int: в функцию придёт число, а не строка.
@app.route('/menu/<int:id>')
def dish(id):
    return f'Dish id is {id}'


# Конвертер any(...) допускает только перечисленные значения.
@app.route('/status/<any(pending, active):status>') # status (pending, active)
def check_status(status):
    return f'status is {status}'


# Два свободных сегмента; конвертер по умолчанию — string (без слеша внутри).
@app.route('/<category>/<sub>')
def dish_cat(category, sub):
    return f'Dish category is {category} and sub is {sub}'


# Ещё один статический маршрут.
@app.route('/events')
def events():
    return 'Events of MyCafe'


# Точка входа: запускаем сервер только при прямом вызове файла.
if __name__ == '__main__':
    # debug=True включает автоперезагрузку при правке кода и подробную страницу ошибки.
    # В продакшене debug обязан быть выключен — он даёт доступ к интерактивной консоли.
    app.run(debug=True)
