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
        return f"User: {self.name}"


@login_manager.user_loader()
def load_user(id):
    return User.query.filter(User.id == id).first()


class Loginform(FlaskForm):
    name = StringField("User name")
    password = PasswordField("Password")
    remember = BooleanField('Remember me')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = url_for(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url


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
