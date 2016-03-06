# -*- coding: UTF-8 -*-

from random import randint

from flask import Flask, request
from flask.ext.assets import Environment, Bundle
from yelp import errors
from app_helpers import debug_state, render_template, scss
from app_helpers import yelp_client_kwargs
from pickabar.api import YelpClient

app = Flask(__name__)
app.debug = debug_state()

assets = Environment(app)
assets.register("css_all", Bundle(
    "css/bootstrap.min.css",
    "sass/app.scss",
    filters=[scss, "cssmin"],
    output="css/pick.a.css"))

yclient = YelpClient(**yelp_client_kwargs())

@app.route("/give-me-that-bar", methods=["POST"])
def show_bar():
    location = request.form.get("location")
    if not location:
        return render_template("home.html", error=True)
    try:
        bars = yclient.search_bars(location)
    except errors.UnavailableForLocation:
        return render_template("bar.html")

    bar = None
    if bars.businesses:
        bar = bars.businesses[randint(0, len(bars.businesses))]

    return render_template("bar.html", bar=bar)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
