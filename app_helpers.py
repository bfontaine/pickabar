# -*- coding: UTF-8 -*-

import os.path
from os import environ
from flask import render_template as _render_template
import sass

here = os.path.dirname(os.path.realpath(__file__))
sass_path = os.path.join(here, "static", "sass")

def debug_state():
    return "PICKABAR_DEBUG" in environ

def render_template(name, **kwargs):
    if "page_id" not in kwargs and name.endswith(".html"):
        kwargs["page_id"] = name.replace(".html", "")

    return _render_template(name, **kwargs)

def scss(_in, out, **kw):
    """sass compilation"""
    out.write(sass.compile(string=_in.read(), include_paths=(sass_path,)))
