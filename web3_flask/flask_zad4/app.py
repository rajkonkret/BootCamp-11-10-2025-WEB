import os
#  pip install -r requirements.txt
from flask import Flask, url_for, request, redirect, render_template, flash

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
        self.denied_codes = []

    def load_offer(self):
        """
        Ładuje dostępne marki samochodów do spinnera
        :return:
        """
        self.brands.append(CarBrand("BMW", "BMW", 'cars/bmw.svg'))
        self.brands.append(CarBrand("Audi", "Audi", 'cars/audi.svg'))
        self.brands.append(CarBrand("Toyota", "Toyota", 'cars/toyota.svg'))
        self.brands.append(CarBrand("Mercedes", "Mercedes", 'cars/mercedes.svg'))

        # zablokowane marki
        self.denied_codes.append('LADA')

    def get_by_code(self, code):
        """
        Zwraca obiekt CarBrand na podstawie marki
        :param code:
        :return:
        """
        for brand in self.brands:
            if brand.code == code:
                return brand

        return CarBrand("UNKNOWN", "Unknown", "cars/unknown.svg")


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
    offer = CarBrandsOffer()
    offer.load_offer()

    if request.method == 'GET':

        # return render_template('create_offer.html')
        return render_template('create_offer.html', offer=offer)
    else:
        print("Jestem w create_offer")
        brand = request.form.get("brand", "BMW")

        price = request.form.get("price", "0")

        if brand in offer.denied_codes:
            flash(f"The brand {brand} cannot be accepted")
        elif offer.get_by_code(brand) == "unknown":
            flash("The selected brand is unknown and cannot be accepted")
        else:
            flash(f"Request to process: {brand} was accepted")

        # return f"<h1>You selected: {brand} price: {price}"
        # przekierowujemy aplikację do endpointa
        # return redirect(
        #     url_for("offer", brand=brand, price=int(price))
        # )
        return render_template(
            "exchange_offer.html",
            brand=brand,
            price=price,
            offer_info=offer.get_by_code(brand)
        )


if __name__ == '__main__':
    app.run(debug=True)
