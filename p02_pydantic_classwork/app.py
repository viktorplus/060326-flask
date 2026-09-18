# Классная работа к уроку 03.09 — та же тема, что в l02_pydantic_models,
# но это отдельное, самостоятельно написанное решение. Чем отличается от урока —
# см. SCHEMA.md рядом.
#
# Запускать из каталога проекта:
#     cd p02_pydantic_classwork
#     python app.py

from flask import Flask, jsonify, Response
from pydantic import ValidationError

# Импорт соседнего модуля — абсолютный, без имени пакета.
# Раньше здесь стояло `from cw1.models import User` — по старому имени каталога,
# и после переименования проект падал с ModuleNotFoundError: No module named 'cw1'.
# Так работает из любого каталога с любым именем: Python кладёт каталог
# запускаемого скрипта в sys.path, поэтому models.py рядом виден.
from models import User

app = Flask(__name__)


@app.route('/')
def index():
    json_string = """{
        "id": 1,
        "name": "John Doe",
        "age": 22.0,
        "email": "john.doe@gmail.com",
        "is_active": 0,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": "123"
        }
    }"""

    # Заметки с занятия: в нестрогом режиме Pydantic делает «безопасные» приведения.
    # bool - int    -> 0/1 превращается в False/True
    # int - float   -> 22.0 превращается в 22
    #
    # Домен gmail.com выбран не случайно: валидатор check_email в models.py пропускает
    # только gmail.com и yahoo.com. Подставьте другой домен — и увидите ветку except.

    try:
        user = User.model_validate_json(json_string, strict=False)
        print(user)
        user.age += 10
        res = user.model_dump_json(indent=4)
        return Response(res, mimetype='application/json')
    except ValidationError as e:
        # Здесь были ДВЕ частые ошибки подряд, обе давали 500 и обе всплывали
        # только тогда, когда валидация реально не проходила.
        #
        # Ошибка 1. errors — это МЕТОД, а не свойство. Без скобок в jsonify попадёт
        # сам объект метода: "TypeError: Object of type builtin_function_or_method
        # is not JSON serializable". Так НЕ надо:
        # return jsonify(e.errors)
        #
        # Ошибка 2. Со скобками — тоже 500: по умолчанию errors() кладёт в ключ 'ctx'
        # исходное исключение валидатора (у нас ValueError из check_email), а объект
        # исключения в JSON не сериализуется. Так тоже НЕ надо:
        # return jsonify(e.errors())
        #
        # Правильно: выключить несериализуемый контекст и вернуть код 400 —
        # без него Flask отдал бы 200, то есть «всё хорошо» на отказе.
        # Тот же разбор подробнее — в l02_pydantic_models/app.py.
        return jsonify(e.errors(include_url=False, include_context=False)), 400


@app.route('/menu')
def menu():
    return 'Menu of MyCafe'

@app.route('/menu/<int:id>')
def dish(id):
    return f'Dish id is {id}'


@app.route('/status/<any(pending, active):status>') # status (pending, active)
def check_status(status):
    return f'status is {status}'


@app.route('/<category>/<sub>')
def dish_cat(category, sub):
    return f'Dish category is {category} and sub is {sub}'


@app.route('/events')
def events():
    return 'Events of MyCafe'


if __name__ == '__main__':
    app.run(debug=True)
