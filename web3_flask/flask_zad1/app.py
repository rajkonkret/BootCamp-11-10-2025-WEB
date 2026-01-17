# pip install Flask
from flask import Flask

app = Flask(__name__)


# http://127.0.0.1:5000
@app.route("/")
def index():
    return "Hello World"


# http://127.0.0.1:5000/about
@app.route("/about")
def about():
    a = 10
    b = 1
    # return "<h1>We are programers<h1>"
    return f"<h1>We are programers {a / b} <h1>"


# http://127.0.0.1:5001/error - zmieniony port
@app.route("/error")
def error():
    a = 10
    b = 0
    # return "<h1>We are programers<h1>"
    return f"<h1>We are programers {a / b} <h1>"


# http://127.0.0.1:5001/cantor/usd/1345
# http://127.0.0.1:5001/cantor/usd/stopiećdziesiąt
# 127.0.0.1 - - [17/Jan/2026 14:02:04] "GET /cantor/usd/stopiećdziesiąt HTTP/1.1" 404 -
@app.route("/cantor/<string:currency>/<int:amount>")
def cantor(currency, amount):
    """
    Nazwy zmiennych odpowiadają nazwą parametrów w url
    :param currency:
    :param amount:
    :return:
    """
    message = f"<h1>You selected {currency} and {amount}<h1>"
    return message


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # port=5001 inny port
# port standartowy 5000
# we flasku nie istnieje OpenAPI -> http://127.0.0.1:5000/docs
# 127.0.0.1 - - [17/Jan/2026 13:47:18] "GET /docs HTTP/1.1" 404 -
# 404 - brak strony
# z apomoca pin mogę zalogować sie do trybu debug
