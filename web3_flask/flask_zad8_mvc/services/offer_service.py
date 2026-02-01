from web3_flask.flask_zad8_mvc.repository import offer_repo
from spinner import CarBrandsOffer


def create_offer(brand, price, user):
    spinner = CarBrandsOffer()
    spinner.load_offer()

    if brand in spinner.denied_codes:
        return False, "Brand not allowed"

    offer_repo.create(brand, price, user)
    return True, "Offer created"
