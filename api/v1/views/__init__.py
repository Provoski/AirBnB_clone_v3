#!/usr/bin/python3
"""__init__ module"""
from flask import Blueprint


"""Create the Blueprint instance for app_view"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


"""Import the views from the index"""
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
