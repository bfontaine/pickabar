# -*- coding: UTF-8 -*-

from random import randint
from flask import Flask, request, render_template
from app_helpers import debug_state
from pickabar.api import YelpClient

app = Flask(__name__)
app.debug = debug_state()

@app.route("/give-me-that-bar", methods=["POST"])
def show_bar():
    yclient = YelpClient(netrc=True)

    form = request.form
    if "location" not in form:
        return render_template("home.html", error="noloc")

    location = form["location"]

    bars = yclient.search_bars(location)

    if not bars.businesses:
        return render_template("home.html", error="noresults")

    bar = bars.businesses[randint(0, len(bars.businesses))]

    return render_template("bar.html", bar=bar)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
