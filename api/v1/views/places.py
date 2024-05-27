#!/usr/bin/python3
"""
This script handles all requests for place object
"""


from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def places_in_city(city_id):
    """
    Retrieves a list of all Place objects
    """
    cities = storage.all(City)

    places_in_city = []
    for city in cities.values():
        if city.id == city_id:
            for place in city.places:
                places_in_city.append(place.to_dict())
            return places_in_city
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def place(place_id):
    """
    Retrieves a specific place using its id
    """
    places = storage.all(Place)

    for place in places.values():
        if place.id == place_id:
            return place.to_dict()
    abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """
    Deletes a specific place from the places objects
    """
    places = storage.all(Place)

    for place in places.values():
        if place.id == place_id:
            storage.delete(place)
            return {}, 200
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """
    Creates an new Place object and stores it
    """
    cities = storage.all(City)
    c = False

    for city in cities.values():
        if city.id == city_id:
            c = True
    if not c:
        abort(404)
    fields = request.get_json()
    if not fields:
        abort(400, "Not a JSON")
    name = fields.get("name")
    user_id = fields.get("user_id")
    if not user_id:
        abort(400, "Missing user_id")
    users = storage.all(User)
    u = False
    for user in users.values():
        if user.id == user_id:
            u = True
    if not u:
        abort(404)

    if not name:
        abort(400, "Missing name")
    fields["city_id"] = city_id
    place = Place(**fields)
    place.save()
    storage.save()
    return place.to_dict(), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """
    Updates a place object
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            fields = request.get_json()
            if not fields:
                return "Not a JSON", 400
            for k, v in fields.items():
                if k == "name":
                    place.name = v
                if k == "price_by_night":
                    place.price_by_night = v
                if k == "max_guest":
                    place.max_guest = v
                if k == "number_rooms":
                    place.number_rooms = v
                if k == "number_bathrooms":
                    place.number_bathrooms = v
                if k == "description":
                    place.description = v
                if k == "longitude":
                    place.longitude = v
                if k == "latitude":
                    place.latitude = v
            place.save()
            storage.save()
            return place.to_dict(), 200
    abort(404)
