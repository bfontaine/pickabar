# -*- coding: UTF-8 -*-

import os.path
from os import environ
from flask import render_template as _render_template
import sass

here = os.path.dirname(os.path.realpath(__file__))
sass_path = os.path.join(here, "static", "sass")

def debug_state():
    return "PICKABAR_DEBUG" in environ

def yelp_client_kwargs():
    kw = {}
    # Set this to use .netrc for local testing
    if environ.get("PICKABAR_NETRC"):
        kw["netrc"] = True
    else:
        kw["env"] = True
    return kw

def bar_address(bar):
    """
    Return the address of a bar
    """
    # Yelp puts the neighbourhood in the display_address even if it has nothing
    # to do there. Their website show the correct address.
    lines = bar.location.display_address[:]
    neighborhoods = bar.location.neighborhoods
    # Hopefully there are no false-positives
    if neighborhoods and neighborhoods[0] in lines:
        lines.remove(neighborhoods[0])

    # Remove the country
    return lines[:-1]

def render_template(name, **kwargs):
    if "page_id" not in kwargs and name.endswith(".html"):
        kwargs["page_id"] = name.replace(".html", "")

    return _render_template(name, **kwargs)

def make_json_serializable(obj):
    """
    A very simple solution to make a JSON-serializable dict of any given
    object. We use it to store stuff in the session for easier debugging.

    It doesn't support loops.
    We're not trying to make a fool-proof solution; just some quick debugging
    tool.
    """
    if isinstance(obj, (list, tuple)):
        ls = []
        for e in obj:
            ls.append(make_json_serializable(e))
        # always use list/tuple classes even if the original object's class
        # inherits from them
        klass = list if isinstance(obj, list) else tuple
        return klass(ls)

    serializables = (None.__class__, str, unicode, bool, int, long, float, dict)
    if isinstance(obj, serializables):
        return obj

    if isinstance(obj, (lambda: 0).__class__):
        raise ValueError(repr(obj) + " can't be JSON serialized")

    d = {}
    for attr in dir(obj):
        if attr.startswith("_"):
            continue
        v = getattr(obj, attr)
        # test if it's JSON-serializable. Note we don't detect loops here
        d[attr] = make_json_serializable(v)

    return d

def scss(_in, out, **kw):
    """sass compilation"""
    out.write(sass.compile(string=_in.read(), include_paths=(sass_path,)))
