# -*- coding: UTF-8 -*-

# "bars" subcategories extracted from:
# https://www.yelp.com/developers/documentation/v2/all_category_list
# Too-specific subcategories were removed, and titles were fixed to be plural.
_categories = {
    # category => title
    "beerbar": "Beer Bars",
    "champagne_bars": "Champagne Bars",
    "cocktailbars": "Cocktail Bars",
    "gaybars": "Gay Bars",
    "lounges": "Lounges",
    "pubs": "Pubs",
    "sportsbars": "Sports Bars",
    "wine_bars": "Wine Bars",
}

def get_categories():
    # make a copy so that the caller can't change the original dict
    return dict(_categories)
