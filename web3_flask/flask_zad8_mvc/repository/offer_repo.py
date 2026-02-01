from web3_flask.flask_zad8_mvc.models import Offer, db


def get_all():
    return Offer.query.all()


def get_by_id(offer_id):
    return Offer.query.get(offer_id)


def create(brand, price, user):
    offer = Offer(brand=brand, price=price, user=user)
    db.session.add(offer)
    db.session.commit()
    return offer


def update(offer, brand, price):
    offer.brand = brand
    offer.price = price
    db.session.commit()


def delete(offer):
    db.session.delete(offer)
    db.session.commit()
