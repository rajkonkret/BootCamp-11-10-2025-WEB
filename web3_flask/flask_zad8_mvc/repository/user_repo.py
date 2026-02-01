from web3_flask.flask_zad8_mvc.models import User
# web3_flask.flask_zad8_mvc.models

def get_by_name(name):
    return User.query.filter_by(name=name).first()


def get_all():
    return User.query.all()
