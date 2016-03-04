# -*- coding: UTF-8 -*-

import json as _json
from os import environ
from flask import Response

from pickabar.bars import get_categories

def debug_state():
    return "PICKABAR_DEBUG" in environ

def json(what, code=200):
    return Response(_json.dumps(what), code, mimetype='application/json')

def json_error(msg, code=400):
    return json({"error": msg}, code=code)

def parse_categories(text):
    if not text:
        return {}
    cats = _json.loads(text)
    categories = get_categories()
    return {c: bool(v) for c, v in cats.items() if c in categories}

def bar_to_dict(bar):
    simple_keys = ["display_phone", "image_url", "is_closed", "name", "phone",
            "rating", "url", "review_count", "rating_img_url"]

    d = {k: getattr(bar, k) for k in simple_keys}

    loc_keys = ["city", "address", "country_code", "display_address",
            "geo_accuracy", "neighborhoods", "postal_code", "state_code"]
    location = bar.location

    d["location"] = {k: getattr(location, k) for k in loc_keys}
    d["location"].update({
        "latitude": location.coordinate.latitude,
        "longitude": location.coordinate.longitude,
    })

    return d
