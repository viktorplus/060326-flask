from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    return 'Index Page'
@app.route('/menu')
def menu():
    return 'Menu Page'

@app.route('/menu/<int:id>')
def dish(id):
    return f'Dish id is {id}'

@app.route('/status/<any(pending, active):status>')
def check_status(status):
    return f'Status is {status}'

@app.route('/<category>/<sub>')
def dish_cat(category, sub):
    return f'Dish category is: {category} and sub is {sub}'









@app.route('/<name>')
def hello_name(name):
    return 'Hello, ' + name + '!'

if __name__ == '__main__':
    app.run()
