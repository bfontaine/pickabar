# -*- coding: UTF-8 -*-

from os import environ

def debug_state():
    return "PICKABAR_DEBUG" in environ
