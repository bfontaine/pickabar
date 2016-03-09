# -*- coding: UTF-8 -*-

"""
Thin wrapper around Yelp's client library.
"""

from os import environ
from netrc import netrc
from random import randint
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

__all__ = ["YelpClient"]

MAX_OFFSET = 1000
DEFAULT_LIMIT = 20

def env_key_variants(k):
    upcase = k.upper()
    return [
        k,
        upcase,
        "YELP_%s" % upcase,
        "PICKABAR_%s" % upcase,
        "PICKABAR_YELP_%s" % upcase,
    ]

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

    def search_bars(self, location, **kwargs):
        """
        Search for bars at a specific location.
        """
        kwargs["category_filter"] = "bars"
        kwargs["location"] = location
        return self.search(**kwargs)

    def get_random_bar(self, location, **kwargs):
        """
        Return a random bar at a given location using max. two requests to the
        Yelp API.
        It first makes an API call in order to get the total results count,
        then generates a random offset under this upper limit. If this offset
        is lower than 20 we already have the business from our API call and can
        return it; if not we make another call to get it.
        """
        kwargs["offset"] = 0
        kwargs["limit"] = DEFAULT_LIMIT
        res = self.search_bars(location, **kwargs)
        if not res.total:
            return None
        max_offset = min(res.total, MAX_OFFSET)
        offset = randint(0, max_offset-1)
        if offset < DEFAULT_LIMIT:
            return res.businesses[offset]
        kwargs["offset"] = offset
        kwargs["limit"] = 1
        res = self.search_bars(location, **kwargs)
        if not res.businesses:
            return None
        return res.businesses[0]
