from flask import Flask, jsonify, Response
from pydantic import ValidationError
from cw1.models import User
app = Flask(__name__)


@app.route('/')
def index():
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

    # bool - int
    # int - float

    try:
        user = User.model_validate_json(json_string, strict=False)
        print(user)
        user.age += 10
        res = user.model_dump_json(indent=4)
        return Response(res, mimetype='application/json')
    except ValidationError as e:
        return jsonify(e.errors)


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
