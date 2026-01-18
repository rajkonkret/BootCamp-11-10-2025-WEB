import os

from flask import Flask, url_for, request, redirect

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
    Add new <a href="{url_for('create_offer')}">offer</a><br>
    Add Audi 10000 go <a href="{url_for('offer', brand="Audi", price=10000)}">here</a><br>
    <img src="{url_for('static', filename='1.svg')}"  alt="Sample"><br>
    <img src="{url_for('static', filename='cars/audi.svg')}"  alt="Audi"><br>
    {url_for('static', filename='cars/audi.svg')}<br>
    {os.path.join(app.static_folder, 'cars/audi.svg')}
    """
    # /static/cars/audi.svg
    # /Users/radoslawjaniak/BootCamp-11-10-2025-WEB/web3_flask/flask_zad3/static/cars/audi.svg
    return f"<h1>Car Ads Portal</h1><br>{menu}"


# http://127.0.0.1:5000/offer/audi/1000
@app.route('/offer/<string:brand>/<int:price>')
def offer(brand, price):
    return f"<h1>You selected: {brand} price: {price}"


@app.route("/create_offer", methods=['GET', 'POST'])
def create_offer():
    # <form action="{url_for("exchange_offer")}" method="POST">
    if request.method == 'GET':
        body = f"""
        <h1>Create Offer</h1>
        <form action="{url_for("create_offer")}" method="POST">
            <label>Car brand</label><br>
            <input type="text" name="brand" value="BMW"<br><br>
            
            <label>Price</label><br>
            <input type="number" name="price" value="50000"><br><br>
    
            <input type="submit" value="Create Offer">
            <br><a href="{url_for('index')}">Back to Home</a>
        """
        return body
    else:
        print("Jestem w create_offer")
        brand = request.form.get("brand", "BMW")

        price = request.form.get("price", "0")

        # return f"<h1>You selected: {brand} price: {price}"
        # przekierowujemy aplikację do endpointa
        return redirect(
            url_for("offer", brand=brand, price=int(price))
        )


# @app.route("/exchange_offer", methods=['POST'])
# def exchange_offer():
#     # brand = "BMW"
#     # if 'brand' in request.form:
#     #     brand = request.form['brand']
#     brand = request.form.get("brand", "BMW")
#
#     price = request.form.get("price", "0")
#
#     # return f"<h1>You selected: {brand} price: {price}"
#     # przekierowujemy aplikację do endpointa
#     return redirect(
#         url_for("offer", brand=brand, price=int(price))
#     )


if __name__ == '__main__':
    app.run(debug=True)
