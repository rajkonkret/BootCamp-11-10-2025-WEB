from flask import Blueprint, render_template, request, redirect, url_for, flash
from web3_flask.flask_zad8_mvc.services.offer_service import create_offer
from web3_flask.flask_zad8_mvc.repository.offer_repo import get_all, get_by_id, delete

offer_bp = Blueprint("offer", __name__)


@offer_bp.route("/history")
def history():
    offers = get_all()
    return render_template('history.html', offers=offers)


@offer_bp.route("create_offer", methods=['GET', "POST"])
def create():
    if request.method == "POST":
        brand = request.form.get("brand", '')
        price = request.form.get("price", '')

        ok, msg = create_offer(brand, price, 'admin')
        flash(msg)

        return redirect(url_for("offer.history"))

    return render_template('create_offer.html')
