import bcrypt

#  pip install -r requirements.txt
from flask import Flask, url_for, request, redirect, render_template, flash, g, session
from flask_sqlalchemy import SQLAlchemy

# app_info = {
#     'db_file': 'data/car_ads_portal.db'
# }

app = Flask(__name__)
# dodajemy secret_key aby działały flash
# app.config['SECRET_KEY'] = "KluczTrudnyDoZlamania"
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


# przy uzyciu flak-sqlalchemy nie jest to potrzebne
# # Singleton
# def get_db():
#     if not hasattr(g, 'sqlite_db'):
#         conn = sqlite3.connect(app_info['db_file'])
#         conn.row_factory = sqlite3.Row  # dostaniemy słownik
#         g.sqlite_db = conn
#
#     return g.sqlite_db
#
#
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
#

# klasa Offer
class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.Text)
    price = db.Column(db.Integer)
    user = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.Text)
    is_active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())


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
    login = UserPass(session.get('user'))
    login.get_user_info()
    return render_template('index.html', login=login, active_menu="home")


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
        price=price,
        login=login,
        active_menu="history"
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
        return render_template('create_offer.html',
                               offer=offer,
                               login=login,
                               active_menu="create_offer")
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
            # db = get_db()
            # sql_commnd = "INSERT INTO offers(brand, price, user) VALUES (?,?,?)"
            # db.execute(sql_commnd, (brand, price, 'admin'))
            # db.commit()
            new_offer = Offer(brand=brand, price=price, user='admin')
            db.session.add(new_offer)
            db.session.commit()

            flash(f"Request to process: {brand} was accepted")

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

    # db = get_db()
    # sql_command = "SELECT id, brand, price FROM offers;"
    # cur = db.execute(sql_command)
    # offers = cur.fetchall()
    offers = Offer.query.all()

    return render_template("history.html",
                           offers=offers,
                           login=login,
                           active_menu="history")


@app.route("/edit_offer/<int:offer_id>", methods=['GET', 'POST'])
def edit_offer(offer_id):
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('login'))

    # db = get_db()
    spinner = CarBrandsOffer()
    spinner.load_offer()

    if request.method == "GET":
        # sql_command = "SELECT id, brand, price FROM offers WHERE id=?"
        # cur = db.execute(sql_command, (offer_id,))
        # offer = cur.fetchone()  # pobranie jednego rekordu

        # offer = Offer.query.filter(Offer.id == offer_id).first()
        offer = Offer.query.get(offer_id)  # Offer.id == offer_id
        print(offer)

        if offer == None:
            flash("No such offer!")
            return redirect(url_for('history'))
        else:
            return render_template("edit_offer.html",
                                   offer=offer,
                                   spinner=spinner,
                                   login=login,
                                   active_menu="history")
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

        # db = get_db()
        # sql_commnd = """
        # UPDATE offers SET
        # brand=?,
        # price=?,
        # user=?
        # WHERE id=?;
        # """
        # db.execute(sql_commnd, (brand, price, 'admin', offer_id))
        # db.commit()
        offer = Offer.query.filter(Offer.id == offer_id)
        offer.brand = brand
        offer.price = price
        offer.user = 'admin'
        db.session.commit()

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

    # db = get_db()
    # sql_command = "DELETE FROM offers WHERE id=?"
    # db.execute(sql_command, (offer_id,))
    # db.commit()
    del_tran = Offer.query.filter(Offer.id == offer_id)
    db.session.delete(del_tran)
    db.session.commit()

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

    # db = get_db()

    # sql_command = "SELECT id, brand, price FROM offers WHERE id=?"
    # cur = db.execute(sql_command, (offer_id,))
    # offer = cur.fetchone()  # pobranie jednego rekordu
    offer = Offer.query.filter(Offer.id == offer_id).first()
    print(offer)

    if offer is None:
        flash("No such offer!")
        return redirect(url_for('history'))
    else:
        return render_template('view_offer_details.html',
                               offer_data=offer,
                               spinner=spinner,
                               login=login,
                               active_menu="history")


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
        # db = get_db()
        # print(self.user, self.password)
        #
        # sql_statement = 'SELECT id, name, password, is_active, is_admin FROM users WHERE name=?'
        # cur = db.execute(sql_statement, (self.user,))
        # user_record = cur.fetchone()
        user_record = User.query.filter(User.name == self.user).first()
        print(user_record)

        # print(user_record['password'], self.password)

        # if user_record is not None and self.verify_password(user_record['password'], self.password):
        if user_record is not None and self.verify_password(user_record.password, self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None

    def get_user_info(self):
        # db = get_db()
        # sql_statement = 'SELECT name, email, is_active, is_admin FROM users WHERE name=?'
        # cur = db.execute(sql_statement, (self.user,))
        # db_user = cur.fetchone()
        db_user = User.query.filter(User.name == self.user).first()
        print(db_user)

        # if db_user is None:
        #     self.is_valid = False
        #     self.is_admin = False
        #     self.email = ''
        # elif db_user['is_active'] != 1:
        #     self.is_admin = False
        #     self.is_valid = False
        #     self.email = db_user['email']
        # else:
        #     self.is_valid = True
        #     self.is_admin = db_user['is_admin']
        #     self.email = db_user['email']
        if db_user is None:
            self.is_valid = False
            self.is_admin = False
            self.email = ''
        elif db_user.is_active != 1:
            self.is_admin = False
            self.is_valid = False
            self.email = db_user.email
        else:
            self.is_valid = True
            self.is_admin = db_user.is_admin
            self.email = db_user.email


@app.route("/login", methods=['GET', 'POST'])
def login():
    login = UserPass(session.get('user'))
    login.get_user_info()

    if request.method == "GET":
        return render_template('login.html', login=login, active_menu="login")
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
            return render_template('login.html', login=login, active_menu="login")


@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash("You are logget out")

    return redirect(url_for('login'))


@app.route('/users')
def users():
    # return "not implemented"
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('login'))

    # db = get_db()
    # sql_command = "SELECT id, name, email, is_admin, is_active FROM users;"
    # cur = db.execute(sql_command)
    # users = cur.fetchall()
    users = User.query.all()

    return render_template('users.html', users=users, login=login, active_menu="users")


@app.route('/edit_user/<user_name>', methods=['GET', 'POST'])
def edit_user(user_name):
    # return "not implemented"
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('login'))

    # db = get_db()
    spinner = CarBrandsOffer()
    spinner.load_offer()

    # sql_command = "SELECT id, name, email, is_active, is_admin FROM users WHERE name=?"
    # cur = db.execute(sql_command, (user_name,))
    # user_record = cur.fetchone()  # pobranie jednego rekordu
    user_record = User.query.filter(User.name == user_name).first()
    print(user_record)

    if offer is None:
        flash("No such user!")
        return redirect(url_for('users'))

    if request.method == "GET":
        return render_template("edit_user.html",
                               user=user_record,
                               spinner=spinner,
                               login=login,
                               active_menu="users")
    else:
        # return "not implemented"
        # user_name, email, user_pass
        print(request.form)
        new_name = request.form.get('user_name', '')
        new_password = request.form.get('user_pass', '')
        new_email = request.form.get('email', '')

        if new_email != user_record['email']:
            # sql_statement = "UPDATE users SET email=? WHERE name=?;"
            # db.execute(sql_statement, (new_email, user_name))
            # db.commit()
            user_record.email = new_email
            db.session.commit()

            flash("Email was changed")

        if new_password != "":
            user_pass = UserPass(user_name, new_name)
            # sql_statement = "UPDATE users SET password=? WHERE name=?;"
            # db.execute(sql_statement, (user_pass.hash_password(new_password), user_name))
            # db.commit()

            user_record.password = user_pass.hash_password(new_password)
            db.session.commit()

            flash("Password was changed")

        return redirect(url_for('users'))


# na wzór tego
# # delete jako metoda POST, gdy używamy modal
# @app.route("/delete_offer/<int:offer_id>", methods=["POST"])
# def delete_offer(offer_id):
#     # sprawdzanie czy user jest zalogowany
#     login = UserPass(session.get('user'))
#     login.get_user_info()
#     if not login.is_valid:
#         return redirect(url_for('login'))
#
#     db = get_db()
#     sql_command = "DELETE FROM offers WHERE id=?"
#     db.execute(sql_command, (offer_id,))
#     db.commit()
#
#     return redirect(url_for('history'))

@app.route('/delete_user/<user_name>', methods=["POST"])
def delete_user(user_name):
    # return "not implemented"

    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('login'))

    # db = get_db()
    # sql_command = "DELETE FROM users WHERE name=?"
    # db.execute(sql_command, (user_name,))
    # db.commit()
    # user = User.query.filter(User.name == user_name).first()
    user = User.query.filter_by(name=user_name).first()
    if user:
        flash(f"User {user_name} has been removed")
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('users'))


# {'user_name': 'radek', 'user_pass': 'raj123', 'email': 'rad@wp.pl'}
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    # return "not implemented"
    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('login'))

    # db = get_db()
    message = None
    user = {}  # słownik

    if request.method == 'GET':
        return render_template('new_user.html', user=user, login=login, active_menu="users")
    else:
        # return "not implemented"
        # user_name, email, user_pass
        print(request.form)
        user['user_name'] = request.form.get('user_name', '')
        user['user_pass'] = request.form.get('user_pass', '')
        user['email'] = request.form.get('email', '')

        print(user)

        # cur = db.execute("SELECT count(*) as cnt FROM users WHERE name=?;", (user['user_name'],))
        # record = cur.fetchone()
        # is_user_name_unique = (record['cnt'] == 0)
        is_user_name_unique = (User.query.filter(User.name == user['user_name']).count() == 0)

        # cur = db.execute("SELECT count(*) as cnt FROM users WHERE email=?;", (user['email'],))
        # record = cur.fetchone()
        # is_user_email_unique = (record['cnt'] == 0)
        is_user_email_unique = (User.query.filter(User.email == user['email']).count() == 0)

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
            # sql_statement = """
            # INSERT INTO users (name, email, password, is_active, is_admin)
            # VALUES(?,?,?,True,False);
            # """
            #
            # db.execute(sql_statement, (user['user_name'], user['email'], password_hash))
            # db.commit()
            new_user = User(
                name=user['user_name'],
                email=user['email'],
                password=password_hash,
                is_active=True,
                is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()

            flash(f"User {user['user_name']} created")
            return redirect(url_for('users'))
        else:
            flash(f"Correct error: {message}")
            return render_template("new_user.html", user=user, login=login, active_menu="users")


@app.route("/user_status_change/<action>/<user_name>")
def user_status_change(action, user_name):
    # login = UserPass(session.get('user'))
    # login.get_user_info()

    # sprawdzanie czy user jest zalogowany
    login = UserPass(session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('login'))

    # db = get_db()

    if action == "active":
        # db.execute("""
        # UPDATE users SET is_active = (is_active + 1) % 2
        # WHERE name=? and name <> ?;""",
        #            (user_name, login.user))
        # db.commit()
        user = User.query.filter(User.name == user_name, User.name != login.user).first()
        if user:
            user.is_active = (user.is_active + 1) % 2
            db.session.commit()
    elif action == "admin":
        # db.execute("""
        #        UPDATE users SET is_admin = (is_admin + 1) % 2
        #        WHERE name=? and name <> ?;""",
        #            (user_name, login.user))
        # db.commit()
        user = User.query.filter(User.name == user_name, User.name != login.user).first()
        if user:
            user.is_admin = (user.is_admin + 1) % 2
            db.session.commit()

    return redirect(url_for('users'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
