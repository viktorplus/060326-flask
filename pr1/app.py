from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "text": "Hello, World!"
    })

@app.route("/hello/<name>")
def hello(name):
    return jsonify({
        "message": f"Hello, {name}!"
    })

@app.route('/double/<int:number>')
def double_number(number):
    return jsonify({
        "number": number,
        "doubled": number * 2
    })

@app.route('/square/<float:number>')
def square_number(number):
    return jsonify({
        "number": number,
        "square": number * number
    })

@app.route('/reverse/<path:text>')
def reverse_text(text):
    return jsonify({
        "original": text,
        "reversed": text[::-1]
    })

if __name__ == "__main__":
    app.run()