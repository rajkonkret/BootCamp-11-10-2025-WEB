from flask import Flask

app = Flask(__name__)


# http://127.0.0.1:5000/
@app.route("/")
def index():
    return f"<h1>Car Ads Portal</h1>"


# http://127.0.0.1:5000/offer/audi/1000
@app.route('/offer/<string:brand>/<int:price>')
def offer(brand, price):
    return f"<h1>You selected: {brand} price: {price}"


if __name__ == '__main__':
    app.run(debug=True)
