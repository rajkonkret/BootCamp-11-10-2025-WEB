from flask import Flask, url_for

app = Flask(__name__)


# http://127.0.0.1:5000/
@app.route("/")
def index():
    # menu = f"""
    #     Add new <a href="">offer</a><br>
    #     Add Audi 10000 go <a href="offer/Audi/10000">here</a><br>
    #     <img src="1.svg" alt="1.svg" alt="Sample"><br>
    #     """
    menu = f"""
    Add new <a href="">offer</a><br>
    Add Audi 10000 go <a href="{url_for('offer', brand="Audi", price=10000)}">here</a><br>
    <img src="{url_for('static', filename='1.svg')}" alt="1.svg" alt="Sample"><br>
    <img src="{url_for('static', filename='cars/audi.svg')}" alt="1.svg" alt="Audi"><br>
    """
    return f"<h1>Car Ads Portal</h1><br>{menu}"


# http://127.0.0.1:5000/offer/audi/1000
@app.route('/offer/<string:brand>/<int:price>')
def offer(brand, price):
    return f"<h1>You selected: {brand} price: {price}"


if __name__ == '__main__':
    app.run(debug=True)
