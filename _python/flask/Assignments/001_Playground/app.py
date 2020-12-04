from flask import Flask, render_template
app = Flask(__name__)


@app.route('/play/')
def indexPlay():
    data = {"times": 3}
    return render_template("index.html", times=3, data=data)


@app.route('/play/<int:times>')
def indexPlayTimes(times):
    data = {"times": times, "color": "#1485ee"}
    return render_template("index.html", times=times, color="#1485ee", data=data)


@app.route('/play/<int:times>/<color>')
def indexPlayTimesColor(times, color):
    data = {"times": times, "color": color}
    return render_template("index.html", times=times, color=color, data=data)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(debug=True)
