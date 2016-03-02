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
    pass
