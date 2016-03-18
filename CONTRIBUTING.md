# Contributing Guide

## Local setup

You need Python with `pip` and [`virtualenv`][]. Clone this repo and run the
bootstrap script:

    git clone https://github.com/bfontaine/pickabar.git && cd pickabar
    ./bootstrap.sh

It’ll setup a local environment in `./venv` and install the required `pip`
packages.

You should now be able to start the Web app:

    ./venv/bin/python web/app.py

Open your browser at http://localhost:5000/.

## Environment

Enable the debugging mode by exporting `PICKABAR_DEBUG=1` before (re-)starting
the Web app.

By default it looks in your environment for the Yelp API credentials but you
can tell it to use your `~/.netrc` by exporting `PICKABAR_NETRC=1`. See the
`pickabar/api.py` file for detailed documentation.

[Virtualenv]: https://virtualenv.pypa.io/en/latest/
