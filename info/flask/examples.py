# -*- coding: utf-8 -*-
"""Запускаемые примеры к справочнику Flask.

    cd info/flask
    python examples.py

Ни один пример не поднимает сервер и не занимает порт: запросы идут через
app.test_client() — встроенный клиент Flask, который вызывает приложение
напрямую. Поэтому вывод детерминированный, а Ctrl+C не нужен.
"""
from flask import Flask, Response, abort, jsonify, make_response, request, url_for


def title(n: int, text: str) -> None:
    print(f"\n{'=' * 70}\n{n}. {text}\n{'=' * 70}")


app = Flask(__name__)

# --------------------------------------------------------------------------
# Маршруты: конвертеры путей
# --------------------------------------------------------------------------
@app.route("/")
def index():
    return "Index Page"


@app.route("/menu")
def menu():
    return "Menu Page"


@app.route("/menu/<int:id>")
def dish(id):
    # id придёт именно int, а не str — это сделал конвертер
    return f"Dish id is {id} (тип {type(id).__name__})"


@app.route("/price/<float:value>")
def price(value):
    return f"Price is {value} (тип {type(value).__name__})"


@app.route("/status/<any(pending, active):status>")
def check_status(status):
    return f"Status is {status}"


@app.route("/files/<path:subpath>")
def files(subpath):
    return f"Path is {subpath}"


@app.route("/<category>/<sub>")
def category(category, sub):
    return f"category={category} sub={sub}"


@app.route("/<name>")
def hello_name(name):
    return f"Hello, {name}!"


# --------------------------------------------------------------------------
# Ответы
# --------------------------------------------------------------------------
@app.route("/json/jsonify")
def json_jsonify():
    return jsonify(status="ok", version=1)


@app.route("/json/manual")
def json_manual():
    # Тело уже готовая СТРОКА — jsonify её бы только экранировал
    ready = '{"status": "ok", "source": "готовая строка"}'
    return Response(ready, mimetype="application/json")


@app.route("/json/wrong")
def json_wrong():
    # ТАК НЕ НАДО: словарь уедет через str() с одинарными кавычками
    return Response(str({"status": "ok"}), mimetype="application/json")


@app.route("/created", methods=["POST"])
def created():
    return jsonify(created=True), 201


@app.route("/headers")
def headers():
    resp = make_response(jsonify(ok=True))
    resp.headers["X-Total-Count"] = "42"
    return resp


# --------------------------------------------------------------------------
# Запрос и ошибки
# --------------------------------------------------------------------------
@app.route("/echo", methods=["GET", "POST"])
def echo():
    if request.method == "POST":
        data = request.get_json(silent=True)
        if data is None:
            return jsonify(error="тело не является корректным JSON"), 400
        return jsonify(method="POST", body=data)
    return jsonify(
        method="GET",
        page=request.args.get("page", default=1, type=int),
        tags=request.args.getlist("tag"),
    )


@app.route("/employees/<int:emp_id>")
def employee(emp_id):
    if emp_id != 1:
        abort(404, description="Сотрудник не найден")
    return jsonify(id=1, name="Elena")


@app.errorhandler(404)
def on_not_found(e):
    # Без этого обработчика клиент получил бы HTML-страницу вместо JSON
    return jsonify(error=str(e.description)), 404


client = app.test_client()


def show(method: str, path: str, **kw) -> None:
    r = client.open(path, method=method, **kw)
    body = r.get_data(as_text=True).strip()
    if len(body) > 160:
        body = body[:160] + "..."
    print(f"  {method:4} {path:34} -> {r.status_code}  {r.mimetype:24} {body}")


# --------------------------------------------------------------------------
title(1, "Конвертеры путей: что куда попадает")

show("GET", "/")
show("GET", "/menu")
show("GET", "/menu/7")
show("GET", "/price/19.99")
show("GET", "/status/active")
show("GET", "/files/a/b/c.txt")
show("GET", "/soup/tomato")
show("GET", "/Viktor")

# --------------------------------------------------------------------------
title(2, "Порядок маршрутов НЕ решает — решает специфичность")

print("  Правила '/menu' и '/<name>' оба подходят под путь /menu.")
show("GET", "/menu")
print("  -> выиграл статический '/menu', хотя '/<name>' объявлен ниже.\n")

print("  '/menu/7' подходит и под '/menu/<int:id>', и под '/<category>/<sub>'.")
show("GET", "/menu/7")
print("  -> выиграл int-конвертер: он специфичнее дефолтного string.\n")

print("  А нецифровой id просто не совпадёт с конвертером int:")
show("GET", "/menu/abc")
print("  -> ушёл в '/<category>/<sub>', а не в dish(). Ошибки нет, просто другое правило.")

print("\n  Путь со слешем внутри не ловится конвертером string:")
show("GET", "/a/b/c")
print("  -> 404: '/<category>/<sub>' не пропускает слеш, для этого есть 'path'.")

# --------------------------------------------------------------------------
title(3, "Таблица маршрутов приложения")

for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
    methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
    print(f"  {rule.rule:34} {methods:10} -> {rule.endpoint}")

# --------------------------------------------------------------------------
title(4, "jsonify против Response: когда что")

show("GET", "/json/jsonify")
print("  -> jsonify сам поставил mimetype и собрал JSON из kwargs\n")

show("GET", "/json/manual")
print("  -> тело было готовой строкой; Response отдал её как есть\n")

show("GET", "/json/wrong")
print("  -> ЛОВУШКА: str(dict) это НЕ JSON — одинарные кавычки, такой ответ не разберётся")

# --------------------------------------------------------------------------
title(5, "Коды ответа и заголовки")

show("POST", "/created")
print("  -> кортеж (тело, код) — самый короткий способ задать статус\n")
show("GET", "/headers")
r = client.get("/headers")
print(f"  свой заголовок X-Total-Count = {r.headers['X-Total-Count']}")

# --------------------------------------------------------------------------
title(6, "Чтение запроса")

show("GET", "/echo?page=3&tag=a&tag=b")
print("  -> args.get(type=int) привёл строку к числу, getlist собрал оба tag\n")

show("POST", "/echo", json={"first_name": "Viktor"})
print("  -> корректный JSON разобран\n")

show("POST", "/echo", data="это не json", content_type="application/json")
print("  -> silent=True вернул None, и мы сами отдали понятный 400 вместо падения")

# --------------------------------------------------------------------------
title(7, "abort + errorhandler: ошибки в том же формате, что и успех")

show("GET", "/employees/1")
show("GET", "/employees/99")
print("  -> без @app.errorhandler(404) здесь приехала бы HTML-страница,")
print("     и клиент, вызывающий response.json(), упал бы на разборе.")

# --------------------------------------------------------------------------
title(8, "url_for: ссылки строятся по имени обработчика")

with app.test_request_context():
    print("  url_for('dish', id=7)                 ->", url_for("dish", id=7))
    print("  url_for('dish', id=7, lang='ru')      ->", url_for("dish", id=7, lang="ru"))
    print("  url_for('menu')                       ->", url_for("menu"))
    print("  -> лишние аргументы уходят в строку запроса, путь берётся из декоратора")

print("\nГотово. Сервер не поднимался: все запросы прошли через app.test_client().")
