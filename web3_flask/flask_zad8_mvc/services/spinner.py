class CarBrand:
    def __init__(self, code, name, logo):
        self.code = code
        self.name = name
        self.logo = logo

    def __repr__(self):
        return f'<CarBrand {self.code}>'


class CarBrandsOffer:

    def __init__(self):
        self.brands = []
        self.denied_codes = []

    def load_offer(self):
        """
        Ładuje dostępne marki samochodów do spinnera
        :return:
        """
        self.brands.append(CarBrand("BMW", "BMW", 'cars/bmw.svg'))
        self.brands.append(CarBrand("Audi", "Audi", 'cars/audi.svg'))
        self.brands.append(CarBrand("Toyota", "Toyota", 'cars/toyota.svg'))
        self.brands.append(CarBrand("Mercedes", "Mercedes", 'cars/mercedes.svg'))

        # zablokowane marki
        self.denied_codes.append('LADA')

    def get_by_code(self, code):
        """
        Zwraca obiekt CarBrand na podstawie marki
        :param code:
        :return:
        """
        for brand in self.brands:
            if brand.code == code:
                return brand

        return CarBrand("UNKNOWN", "Unknown", "cars/unknown.svg")

