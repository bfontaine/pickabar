# -*- coding: UTF-8 -*-

try:
    from urllib import urlencode
except ImportError:  # Python 3
    from urllib.parse import urlencode

from jinja2 import evalcontextfilter, Markup, escape

_osm_default_attrs = dict(
    width=500,
    height=400,
    frameborder=0,
    scrolling="no",
    marginheight=0,
    marginwidth=0,
)

@evalcontextfilter
def osm_map(eval_ctx, loc, **kw):
    lat = loc["latitude"]
    lon = loc["longitude"]
    layer = kw.pop("layer", "mapnik")

    attrs = dict(_osm_default_attrs)
    attrs.update(kw)

    # roughly equivalent to zoom level 17
    # (note: this also depends on the width/height proportions)
    lon_padding = 0.0063589
    lat_padding = 0.00333
    bbox = [lon-lon_padding, lat-lat_padding, lon+lon_padding, lat+lat_padding]

    params = {
            "bbox": ",".join([str(p) for p in bbox]),
            "layer": layer,
            "marker": "%f,%f" % (lat, lon),
    }

    html_attrs = " ".join(
            ['%s="%s"' % (escape(k), escape(v)) for k, v in attrs.items()])

    iframe = '<iframe %s src="http://www.openstreetmap.org/export/embed.html?%s"></iframe>' % (
        html_attrs,
        urlencode(params),
    )

    if eval_ctx.autoescape:
        return Markup(iframe)
    return iframe

@evalcontextfilter
def osm_url(eval_ctx, loc, zoom=16):
    """
    Given a dict-like with ``latitude`` and ``longitude`` attributes write an
    OpenStreetMap URL for this location.
    """
    lat = loc["latitude"]
    lon = loc["longitude"]

    url = "http://www.openstreetmap.org/?mlat=%f&amp;mlon=%f#map=%d/%f/%f" % (
        lat, lon, zoom, lat, lon)

    return url

def activate_filters(app):
    app.jinja_env.filters.update(dict(
        osm_map=osm_map,
        osm_url=osm_url,
    ))
