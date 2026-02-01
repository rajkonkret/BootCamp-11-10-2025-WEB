from datetime import datetime

from flask import Flask
from wtyczka import MojaWtyczka

app = Flask(__name__)
moja_wtyczke = MojaWtyczka(app)

@app.route("/")
def index():
    time_now = datetime.now().strftime("%H:%M:%S")
    print(moja_wtyczke)
    return f"Witaj w mojej aplikacji {time_now}"


if __name__ == '__main__':
    app.run(debug=True, port=5004)
#  pip install waitress
# waitress-serve --host=0.0.0.0 --port=5004 app:app
# http://localhost:5004