# -*- coding: UTF-8 -*-

from flask import Flask, request, redirect, url_for, session
from flask.ext.assets import Environment, Bundle
from yelp import errors
from app_helpers import debug_state, render_template, scss, bar_address
from app_helpers import yelp_client_kwargs, make_json_serializable
from app_helpers import show_apple_maps
from pickabar.api import YelpClient
from jinja2_maps import activate_filters

app = Flask(__name__)
app.debug = debug_state()
app.secret_key = "debug"

activate_filters(app.jinja_env)

assets = Environment(app)
assets.register("css_all", Bundle(
    "css/bootstrap.min.css",
    "sass/app.scss",
    filters=[scss, "cssmin"],
    output="css/pick.a.css"))
assets.register("js_all", Bundle(
    "js/app.js",
    # we don't want to depend on external tools
    filters=["jsmin"],
    output="js/pick.a.js"))

yclient = YelpClient(**yelp_client_kwargs())

@app.route("/give-me-that-bar", methods=["POST"])
def show_bar():
    location = request.form.get("location", "").strip()
    if not location:
        return render_template("home.html", error=True)

    bar = None
    error = None
    try:
        bar = yclient.get_random_bar(location)
    except errors.UnspecifiedLocation:
        return render_template("home.html", error=True)
    except (
        errors.UnavailableForLocation,
        errors.YelpError), e:
        error = e.__class__.__name__

    address = bar_address(bar)

    if app.debug:
        session["bar"] = make_json_serializable(bar)
        session["address"] = address

    return render_template("bar.html", bar=bar, bar_address=address,
            error=error,
            show_apple_maps=show_apple_maps(request))

@app.route("/give-me-that-bar", methods=["GET"])
def get_show_bar():
    if app.debug:
        return render_template("bar.html", bar=session["bar"], title="DEBUG",
                bar_address=session["address"],
                show_apple_maps=show_apple_maps(request))
    return redirect(url_for("home"), code=303)  # See Other

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
