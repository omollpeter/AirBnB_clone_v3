#!/usr/bin/python3
"""
This script is for defining routes using the blueprint instance
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Returns the count of each object stored in db or file
    """
    amenities = storage.count(Amenity)
    users = storage.count(User)
    places = storage.count(Place)
    cities = storage.count(City)
    states = storage.count(State)
    reviews = storage.count(Review)

    return jsonify({
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "states": states,
        "users": users,
        "reviews": reviews
    })
