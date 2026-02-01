import bcrypt
from flask import Flask, render_template, url_for, request, flash, g, redirect, session
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

# konfiguracja z pliku
app.config.from_pyfile("config.cfg")

db = SQLAlchemy(app)  # baza danych

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "First, please log in"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.Text)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))

    def __repr__(self):
        return f"<User {self.name}>"


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


class LoginForm(FlaskForm):
    name = StringField("User name")
    password = PasswordField("Password")
    remember = BooleanField('Remember me')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
            test_url.scheme in ('http', 'https')
            and ref_url.netloc == test_url.netloc
    )


def get_hashed_password(password):
    """
            Hashuje hasłą używając
            :return:
            """

    return (bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt())
            .decode('utf-8'))


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


@app.route("/")
def index():
    return "<h1>Hello!</h1>"


# 127.0.0.1:5000/init
@app.route("/init")
def init():
    db.create_all()

    admin = User.query.filter(User.name == 'admin').first()
    if admin is None:
        admin = User(
            id=1,
            name="admin",
            password=get_hashed_password("Passw0rd"),
            first_name="Radek",
            last_name="Kowalski"
        )

        db.session.add(admin)
        db.session.commit()
        return "<h1>Initial configuration done!</h1>"
    return None


@app.route("/logout")
def logout():
    logout_user()
    return "<h1>You are logged out</h1>"


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # csrf
    if form.validate_on_submit():
        print(form.name.data, form.password.data)

        user = User.query.filter(User.name == form.name.data).first()
        if user is not None and verify_password(user.password, form.password.data):
            login_user(user)

            next = request.args.get('next')
            if next and is_safe_url(next):
                return redirect(next)
            else:
                return "<h1>You are authenticated!</h1>"

    return render_template('login.html', form=form)


@app.route("/docs")
@login_required  # zabezpieczamy endpoint, działa po zalogowaniu
def docs():
    return f"<h1>You have acess to protected docs.</h1>"
    # return f"<h1>You have acess to protected docs. You are {current_user.name}</h1>"


if __name__ == '__main__':
    app.run(debug=True)
