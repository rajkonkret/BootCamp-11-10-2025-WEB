# klasa Offer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.Text)
    price = db.Column(db.Integer)
    user = db.Column(db.Text)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password = db.Column(db.Text)
    is_active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())
