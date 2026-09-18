# Практика по маршрутизации: конвертеры путей и JSON-ответы.
# Относится к уроку l01_routing — там та же тема разобрана на «скелетном» примере,
# здесь она закреплена задачами.

# Flask   — класс приложения.
# jsonify — превращает dict/list в готовый Response с mimetype application/json.
from flask import Flask, jsonify

app = Flask(__name__)


# Статический маршрут без параметров.
@app.route("/")
def home():
    # Возвращаем словарь через jsonify: заголовок Content-Type проставится сам.
    return jsonify({
        "text": "Hello, World!"
    })


# Динамический сегмент без указания конвертера — работает конвертер по умолчанию
# 'string': любой текст БЕЗ слеша внутри.
@app.route("/hello/<name>")
def hello(name):
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Конвертер int: пропускает ТОЛЬКО цифры и отдаёт в функцию int, а не строку.
# Поэтому number * 2 — это арифметика, а не удвоение строки.
@app.route('/double/<int:number>')
def double_number(number):
    return jsonify({
        "number": number,
        "doubled": number * 2
    })


# Конвертер float. ВНИМАНИЕ на две особенности, они проверены запуском:
#   /square/2.5   -> 200
#   /square/4     -> 404  — float требует точку в записи, целое число он не примет;
#   /square/-2.5  -> 404  — отрицательные значения конвертер по умолчанию не пропускает
#                           (у него есть параметр signed=True, но в правиле его нет).
# Это не ошибка приложения: правило просто не совпало, и Flask ищет дальше.
@app.route('/square/<float:number>')
def square_number(number):
    return jsonify({
        "number": number,
        "square": number * number
    })


# Конвертер path — как string, но слеши ВНУТРИ разрешены.
# Поэтому /reverse/a/b/c совпадёт целиком: text = 'a/b/c'.
@app.route('/reverse/<path:text>')
def reverse_text(text):
    # [::-1] — срез с шагом -1, разворачивает строку.
    return jsonify({
        "original": text,
        "reversed": text[::-1]
    })


# Точка входа: сервер поднимается только при прямом запуске файла.
if __name__ == "__main__":
    # Запускать из каталога проекта: cd p01_routing_practice && python app.py
    app.run()
