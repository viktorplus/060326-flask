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
        "email": "john.doe@gmail.com",
        "is_active": 0,
        "address": {
            "city": "New York",
            "street": "5th Avenue",
            "house_number": "123"
        }
    }"""

    # Домен gmail.com выбран не случайно: валидатор check_email в models.py пропускает
    # только gmail.com и yahoo.com. Подставьте любой другой домен (например example.com) —
    # и запрос уйдёт в ветку except ниже. Это удобный способ увидеть обе ветки обработчика.

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

        # Здесь две ЧАСТЫЕ ОШИБКИ подряд, обе дают 500 и обе всплывают только
        # тогда, когда валидация РЕАЛЬНО не прошла — на успешном запросе их не видно.

        # Ошибка 1. errors — это МЕТОД, а не свойство. Без скобок в jsonify попадёт
        # сам объект метода: "TypeError: Object of type builtin_function_or_method
        # is not JSON serializable". Так НЕ надо:
        # return jsonify(e.errors)

        # Ошибка 2. Вызвать метод — мало. По умолчанию errors() кладёт в каждый
        # элемент ключ 'ctx' с ИСХОДНЫМ исключением валидатора (у нас — ValueError
        # из check_email), а объект исключения в JSON не сериализуется:
        # "TypeError: Object of type ValueError is not JSON serializable". Так тоже НЕ надо:
        # return jsonify(e.errors())

        # Правильно: выключить несериализуемый контекст (и заодно ссылку на доки —
        # в теле ответа она не нужна). Тот же приём применён в l03_rest_api/app.py.
        #
        # Вторым элементом кортежа возвращаем код ответа. Без него Flask отдаст 200,
        # то есть «всё хорошо» — на ошибку валидации это неверно: клиент не сможет
        # отличить успех от отказа, не разбирая тело. 400 Bad Request — «данные кривые».
        return jsonify(e.errors(include_url=False, include_context=False)), 400


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
