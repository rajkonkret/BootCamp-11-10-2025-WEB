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


if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # port=5001 inny port
# port standartowy 5000
# we flasku nie istnieje OpenAPI -> http://127.0.0.1:5000/docs
# 127.0.0.1 - - [17/Jan/2026 13:47:18] "GET /docs HTTP/1.1" 404 -
# 404 - brak strony
# z apomoca pin mogę zalogować sie do trybu debug