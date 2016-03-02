# -*- coding: UTF-8 -*-

"""
Thin wrapper around Yelp's client library.
"""

from netrc import netrc
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

__all__ = ["YelpClient"]

class YelpClient(object):
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
    """

    def __init__(self, **kwargs):
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

        self._client = Client(Oauth1Authenticator(**kwargs))
