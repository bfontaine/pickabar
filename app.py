# -*- coding: UTF-8 -*-

from random import randint

from flask import Flask, request
from flask.ext.assets import Environment, Bundle
from app_helpers import debug_state, render_template, scss
from pickabar.api import YelpClient

app = Flask(__name__)
app.debug = debug_state()

assets = Environment(app)
assets.register("css_all", Bundle(
    "css/bootstrap.min.css",
    "sass/app.scss",
    filters=[scss, "cssmin"],
    output="css/pick.a.css"))


@app.route("/give-me-that-bar", methods=["POST"])
def show_bar():
    location = request.form.get("location")
    if not location:
        return render_template("home.html", error=True)
    yclient = YelpClient(netrc=True)
    bars = yclient.search_bars(location)

    bar = None
    if bars.businesses:
        bar = bars.businesses[randint(0, len(bars.businesses))]

    return render_template("bar.html", bar=bar)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
