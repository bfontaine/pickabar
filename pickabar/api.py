# -*- coding: UTF-8 -*-

"""
Thin wrapper around Yelp's client library.
"""

from os import environ
from netrc import netrc
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

__all__ = ["YelpClient"]

def env_key_variants(k):
    upcase = k.upper()
    return [
        k,
        upcase,
        "YELP_%s" % upcase,
        "PICKABAR_%s" % upcase,
        "PICKABAR_YELP_%s" % upcase,
    ]

def filter_categories(businesses, exclude):
    categories = set(exclude)
    filtered = []
    for b in businesses:
        for cat in b.categories:
            if cat.alias in categories:
                break
        else:
            filtered.append(b)

    return filtered


class YelpClient(Client):
    """
    Yelp API client. Keywords arguments for the constructor should be
    ``consumer_key``, ``consumer_secret``, ``token``, ``token_secret``. There
    are passed as-is. If a truthy ``netrc`` is given it'll get the credentials
    from the ``~/.netrc`` file. They should be in the following format: ::

        machine api.yelp.com
            login your_consumer_key:your_consumer_secret
            account your_token
            password your_token_secret

    Replace ``your_*`` strings with the correct values. This file should belong
    to the user running the process and shouldn't be accessible in read or
    write by any other user.

    With the example ``~/.netrc`` above one can call this method like so: ::

        >>> client = YelpClient(netrc=True)

    Otherwise it'll look like this: ::

        >>> client = YelpClient(consumer_key="your_consumer_key",
                consumer_secret="your_consumer_secret", token="your_token",
                token_secret="your_token_secret")

    If ``netrc`` is passed it takes precedence over the other arguments.

    An alternative way of giving the credentials is to pass ``env=True``. In
    that case it'll look for environment keys ``YELP_CONSUMER_KEY``,
    ``YELP_CONSUMER_SECRET``, ``YELP_TOKEN`` and ``YELP_TOKEN_SECRET``. You can
    also use ``PICKABAR_`` as a prefix instead of ``YELP_``.
    """

    def __init__(self, **kwargs):
        keys = ["consumer_key", "consumer_secret", "token", "token_secret"]
        if "netrc" in kwargs and kwargs.pop("netrc"):
            auths = netrc().authenticators("api.yelp.com")
            if auths:
                consumer, token, secret = auths
                key, consumer_secret = consumer.split(":", 1)
                kwargs.update(
                    consumer_key=key,
                    consumer_secret=consumer_secret,
                    token=token,
                    token_secret=secret,
                )
        elif "env" in kwargs and kwargs.pop("env"):
            for k in keys:
                for v in env_key_variants(k):
                    if v in environ:
                        kwargs[k] = environ[v]
                        break

        super(YelpClient, self).__init__(Oauth1Authenticator(**kwargs))

    def search_bars(self, location, categories=None, **kwargs):
        """
        Search for bars at a specific location. If ``categories`` is given it
        must be a ``dict`` mapping category aliases to booleans indicating if
        these should be included or excluded from the results. Categories are
        excluded after the query so you might get fewer results than the limit
        you gave (the default is ``20``).
        """
        include = set(["bars"])
        exclude = []
        if "category_filter" in kwargs:
            include.update(kwargs["category_filter"].split(","))

        if categories:
            for cat, ok in categories.items():
                if ok:
                    include.add(cat)

        kwargs["category_filter"] = ",".join(include)
        kwargs["location"] = location
        resp = self.search(**kwargs)

        if categories:
            exclude = [c for c, ok in categories.items() if not ok]
            resp.businesses = filter_categories(resp.businesses,
                    exclude)

        return resp
