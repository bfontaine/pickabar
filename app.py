# -*- coding: UTF-8 -*-

from flask import Flask, request, render_template
from app_helpers import json, json_error, parse_categories, bar_to_dict
from app_helpers import debug_state
from pickabar.api import YelpClient

app = Flask(__name__)
app.debug = debug_state()

#yclient = YelpClient(env=True)

@app.route("/api/1/json/bars", methods=["POST"])
def json_bars():
    form = request.form
    if "location" not in form:
        return json_error("Missing location")

    location = form["location"]
    try:
        categories = parse_categories(form.get("categories", ""))
    except ValueError:
        return json_error("Bad categories")

    bars = yclient.search_bars(location, categories=categories)
    return json({
        "bars": [bar_to_dict(bar) for bar in bars.businesses],
    })

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
