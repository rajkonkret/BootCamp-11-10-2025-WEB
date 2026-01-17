from flask import Flask, request

app = Flask(__name__)


# http://127.0.0.1:5000
# http://127.0.0.1:5000/?color=blue
# http://127.0.0.1:5000/?color=blue&style=italic
# http://127.0.0.1:5000/?color=blue&style=italic">Hacked<
# http://127.0.0.1:5000/?color=blue&style=italic%22%3EHacked%3C
@app.route("/")
def index():
    # b'color=blue'
    print(request.query_string)
    # print(request.args['color'])

    color = "black"
    if 'color' in request.args:
        color = request.args['color']

    style = "normal"
    if 'style' in request.args:
        style = request.args['style']

    for p in request.args:
        print(p, request.args[p])
    # b'color=blue&style=italic'
    # color blue
    # style italic

    return f'<h1 style="color: {color}; font-style:{style};">Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
