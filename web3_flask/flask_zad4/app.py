import os

from flask import Flask, url_for, request, redirect, render_template

app = Flask(__name__)


class CarBrand:
    def __init__(self, code, name, logo):
        self.code = code
        self.name = name
        self.logo = logo

    def __repr__(self):
        return f'<CarBrand {self.code}>'

class CarBrandsOffer:

    def __init__(self):
        self.brands = []

    def load_offer(self):
        """
        Ładuje dostępne marki samochodów do spinnera
        :return:
        """
        self.brands(CarBrand("BMW", "BMW", 'cars/bmw.svg'))
        self.brands(CarBrand("Audi", "Audi", 'cars/audi.svg'))
        self.brands(CarBrand("Toyota", "Toyota", 'cars/toyota.svg'))


# http://127.0.0.1:5000/
@app.route("/")
def index():
    return render_template('index.html')


# http://127.0.0.1:5000/offer/audi/1000
@app.route('/offer/<string:brand>/<int:price>')
def offer(brand, price):
    # return f"<h1>You selected: {brand} price: {price}</h1>"
    return render_template(
        "exchange_offer.html",
        brand=brand,
        price=price
    )


@app.route("/create_offer", methods=['GET', 'POST'])
def create_offer():
    # <form action="{url_for("exchange_offer")}" method="POST">
    if request.method == 'GET':

        return render_template('create_offer.html')
    else:
        print("Jestem w create_offer")
        brand = request.form.get("brand", "BMW")

        price = request.form.get("price", "0")

        # return f"<h1>You selected: {brand} price: {price}"
        # przekierowujemy aplikację do endpointa
        return redirect(
            url_for("offer", brand=brand, price=int(price))
        )


if __name__ == '__main__':
    app.run(debug=True)
