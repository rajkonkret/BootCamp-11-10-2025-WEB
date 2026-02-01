import bcrypt
from web3_flask.flask_zad8_mvc.repository.user_repo import get_by_name


def authenticate(username, password):
    user = get_by_name(username)
    if not user:
        return None

    if bcrypt.checkpw(password.encode(), user.password.encode()):
        return user

    return None
