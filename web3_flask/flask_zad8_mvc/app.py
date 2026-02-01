from flask import Flask
from models import db
from view.offer_view import offer_bp
from view.auth_view import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.cfg")

    db.init_app(app)

    app.register_blueprint(offer_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5003)
