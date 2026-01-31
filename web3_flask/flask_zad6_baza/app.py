import os
import sqlite3

#  pip install -r requirements.txt
from flask import Flask, url_for, request, redirect, render_template, flash, g

app_info = {
    'db_file': 'data/car_ads_portal.db'
}

app = Flask(__name__)
# dodajemy secret_key aby działały flash
app.config['SECRET_KEY'] = "KluczTrudnyDoZlamania"


# Singleton
def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect(app_info['db_file'])
        conn.row_factory = sqlite3.Row  # dostaniemy słownik
        g.sqlite_db = conn

    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


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
        flash("Debug: starting process in POST mode")
        brand = request.form.get("brand", "BMW")

        price = request.form.get("price", "0")

        if brand in offer.denied_codes:
            flash(f"The brand {brand} cannot be accepted")
        elif offer.get_by_code(brand) == "unknown":
            flash("The selected brand is unknown and cannot be accepted")
        else:
            flash(f"Request to process: {brand} was accepted")

        db = get_db()
        sql_commnd = "INSERT INTO offers(brand, price, user) VALUES (?,?,?)"
        db.execute(sql_commnd, (brand, price, 'admin'))
        db.commit()

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


@app.route("/history")
def history():
    db = get_db()
    sql_command = "SELECT id, brand, price FROM offers;"
    cur = db.execute(sql_command)
    offers = cur.fetchall()

    return render_template("history.html", offers=offers)


@app.route("/edit_offer/<int:offer_id>", methods=['GET', 'POST'])
def edit_offer(offer_id):
    db = get_db()
    spinner = CarBrandsOffer()
    spinner.load_offer()

    if request.method == "GET":
        sql_command = "SELECT id, brand, price FROM offers WHERE id=?"
        cur = db.execute(sql_command, (offer_id,))
        offer = cur.fetchone()  # pobranie jednego rekordu
        print(offer)

        if offer == None:
            flash("No such offer!")
            return redirect(url_for('history'))
        else:
            return render_template("edit_offer.html",
                                   offer=offer,
                                   spinner=spinner)
    else:
        flash("Debug: starting process in POST mode")
        brand = request.form.get("brand", "BMW")

        price = request.form.get("price", "0")

        if brand in spinner.denied_codes:
            flash(f"The brand {brand} cannot be accepted")
        elif spinner.get_by_code(brand) == "unknown":
            flash("The selected brand is unknown and cannot be accepted")
        else:
            flash(f"Request to process: {brand} was accepted")

        db = get_db()
        sql_commnd = """
        UPDATE offers SET
        brand=?,
        price=?,
        user=?
        WHERE id=?;
        """
        db.execute(sql_commnd, (brand, price, 'admin', offer_id))
        db.commit()

        # return f"<h1>You selected: {brand} price: {price}"
        # przekierowujemy aplikację do endpointa
        # return redirect(
        #     url_for("offer", brand=brand, price=int(price))
        # )
        flash("Transaction was updated")

    return redirect(url_for('history'))


# delete jako metoda POST, gdy używamy modal
@app.route("/delete_offer/<int:offer_id>", methods=["POST"])
def delete_offer(offer_id):
    db = get_db()
    sql_command = "DELETE FROM offers WHERE id=?"
    db.execute(sql_command, (offer_id,))
    db.commit()

    return redirect(url_for('history'))


@app.route("/view_offer/<int:offer_id>")
def view_offer(offer_id):
    """
    Wyświetla szczegóy oferty
    :param offer_id:
    :return:
    """
    spinner = CarBrandsOffer()
    spinner.load_offer()

    db = get_db()

    sql_command = "SELECT id, brand, price FROM offers WHERE id=?"
    cur = db.execute(sql_command, (offer_id,))
    offer = cur.fetchone()  # pobranie jednego rekordu
    print(offer)

    if offer is None:
        flash("No such offer!")
        return redirect(url_for('history'))
    else:
        return render_template('view_offer_details.html',
                               offer_data=offer,
                               spinner=spinner)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
