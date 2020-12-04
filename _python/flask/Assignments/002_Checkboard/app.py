from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", x=8, y=8)


@app.route('/<int:y>/')
def indexY(y):
    return render_template("index.html", y=y, x=8)


@app.route('/<int:y>/<int:x>')
def indexYX(y, x):
    return render_template("index.html", y=y, x=x)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(debug=True)
