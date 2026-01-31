import os
import sqlite3
import bcrypt

#  pip install -r requirements.txt
from flask import Flask, url_for, request, redirect, render_template, flash, g, session

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
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

    # return f"<h1>You selected: {brand} price: {price}</h1>"
    return render_template(
        "exchange_offer.html",
        brand=brand,
        price=price
    )


@app.route("/create_offer", methods=['GET', 'POST'])
def create_offer():
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

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
        # return render_template(
        #     "exchange_offer.html",
        #     brand=brand,
        #     price=price,
        #     offer_info=offer.get_by_code(brand)
        # )

        return redirect('history')


@app.route("/history")
def history():
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

    db = get_db()
    sql_command = "SELECT id, brand, price FROM offers;"
    cur = db.execute(sql_command)
    offers = cur.fetchall()

    return render_template("history.html", offers=offers)


@app.route("/edit_offer/<int:offer_id>", methods=['GET', 'POST'])
def edit_offer(offer_id):
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

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
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

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
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

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


# ======= LOGIN ======
class UserPass:

    def __init__(self, user="", password=""):
        self.user = user
        self.password = password
        self.email = ""
        self.is_valid = False
        self.is_admin = False

    # pbkdf2 - starsze hashowanie
    # bcrypt -> scrypt
    # argon2id
    @staticmethod
    def hash_password(password):
        """
        Hashuje hasłą używając
        :return:
        """

        return (bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt())
                .decode('utf-8'))

    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        Weryfikuje hasło
        :param stored_password:
        :param provided_password:
        :return:
        """

        return bcrypt.checkpw(
            provided_password.encode('utf-8'),
            stored_password.encode('utf-8')
        )

    def login_user(self):
        db = get_db()
        print(self.user, self.password)

        sql_statement = 'SELECT id, name, password, is_active, is_admin FROM users WHERE name=?'
        cur = db.execute(sql_statement, (self.user,))
        user_record = cur.fetchone()
        print(user_record)

        print(user_record['password'], self.password)

        if user_record is not None and self.verify_password(user_record['password'], self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None

    def get_user_info(self):
        db = get_db()
        sql_statement = 'SELECT name, email, is_active, is_admin FROM users WHERE name=?'
        cur = db.execute(sql_statement, (self.user,))
        db_user = cur.fetchone()

        if db_user is None:
            self.is_valid = False
            self.is_admin = False
            self.email = ''
        elif db_user['is_active'] != 1:
            self.is_admin = False
            self.is_valid = False
            self.email = db_user['email']
        else:
            self.is_valid = True
            self.is_admin = db_user['is_admin']
            self.email = db_user['email']


@app.route("/login", methods=['GET', 'POST'])
def login():
    login = UserPass(session.get('user'))
    login.get_user_info()

    if request.method == "GET":
        return render_template('login.html', login=login)
    else:
        user_name = request.form.get('user_name', '')
        user_pass = request.form.get('user_pass', '')

        print(user_name, user_pass)

        login = UserPass(user_name, user_pass)
        login_record = login.login_user()

        if login_record is not None:
            session['user'] = user_name
            flash(f"Logon succesfull: {user_name}")
            return redirect(url_for('index'))
        else:
            flash("Login failed, try again")
            return render_template('login.html', login=login)


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash("You are logget out")

    return redirect(url_for('login'))


@app.route('/users')
def users():
    # return "not implemented"
    db = get_db()
    sql_command = "SELECT id, name, email, is_admin, is_active FROM users;"
    cur = db.execute(sql_command)
    users = cur.fetchall()

    return render_template('users.html', users=users)

@app.route('/edit_user/<user_name>', methods=['GET', 'POST'])
def edit_user(user_name):
    return "not implemented"


@app.route('/delete_user/<user_name>')
def delete_user(user_name):
    return "not implemented"

# {'user_name': 'radek', 'user_pass': 'raj123', 'email': 'rad@wp.pl'}
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    # return "not implemented"
    db = get_db()
    message = None
    user = {}  # słownik

    if request.method == 'GET':
        return render_template('new_user.html', user=user)
    else:
        # return "not implemented"
        # user_name, email, user_pass
        print(request.form)
        user['user_name'] = request.form.get('user_name', '')
        user['user_pass'] = request.form.get('user_pass', '')
        user['email'] = request.form.get('email', '')

        print(user)

        cur = db.execute("SELECT count(*) as cnt FROM users WHERE name=?;", (user['user_name'],))
        record = cur.fetchone()
        is_user_name_unique = (record['cnt'] == 0)

        cur = db.execute("SELECT count(*) as cnt FROM users WHERE email=?;", (user['email'],))
        record = cur.fetchone()
        is_user_email_unique = (record['cnt'] == 0)

        if user['user_name'] == "":
            message = "Name cannot be empty"
        elif user['email'] == "":
            message = "Email cannot be empty"
        elif user['user_pass'] == "":
            message = "Password cannot be empty"
        elif not is_user_name_unique:
            message = f"User with the name {user['user_name']} already exists"
        elif not is_user_email_unique:
            message = f"User with the email {user['email']} already exists"

        if not message:
            user_pass = UserPass(user["user_name"], user['user_pass'])
            password_hash = user_pass.hash_password(user['user_pass'])
            sql_statement = """
            INSERT INTO users (name, email, password, is_active, is_admin)
            VALUES(?,?,?,True,False);
            """

            db.execute(sql_statement, (user['user_name'], user['email'], password_hash))
            db.commit()

            flash(f"User {user['user_name']} created")
            return redirect(url_for('users'))
        else:
            flash(f"Correct error: {message}")
            return render_template("new_user.html", user=user)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
