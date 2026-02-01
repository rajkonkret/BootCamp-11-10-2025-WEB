from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from web3_flask.flask_zad8_mvc.services.auth_service import authenticate

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = authenticate(
            request.form.get("user_name", ''),
            request.form.get("user_pass", ''),
        )

        if user:
            session['user'] = user.name
            return redirect(url_for("offer.history"))

        flash("Login failed")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))
