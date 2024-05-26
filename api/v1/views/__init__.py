#!/usr/bin/python3
"""
This is an init file for the views package that contain blueprint for
all the routes
"""


from flask import Blueprint


app_views = Blueprint(
    "app_views", __name__, url_prefix="/api/v1"
)

from api.v1.views.index import *  # To prevent circular import
from api.v1.views.states import *
from api.v1.views.cities import *
