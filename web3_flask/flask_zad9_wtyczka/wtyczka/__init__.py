from flask import Flask


class MojaWtyczka:
    def __init__(self, app: Flask):
        """
        Metoda inicjalizująca
        :param app:
        """
        self.app = app
        self.initialization()

    def initialization(self):
        @self.app.route("/moja-wtyczka")
        def moja_wtyczka():
            return "Witaj z wtyczki"
