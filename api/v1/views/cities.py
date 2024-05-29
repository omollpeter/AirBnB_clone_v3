#!/usr/bin/python3
"""
This script handles all requests for city object
"""


from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def cities_in_state(state_id):
    """
    Retrieves a list of all City objects
    """
    states = storage.all(State)

    cities_in_state = []
    for state in states.values():
        if state.id == state_id:
            for city in state.cities:
                cities_in_state.append(city.to_dict())
            return cities_in_state
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def city(city_id):
    """
    Retrieves a specific city using its id
    """
    cities = storage.all(City)

    for city in cities.values():
        if city.id == city_id:
            return city.to_dict()
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Deletes a specific city from the cities objects
    """
    cities = storage.all(City)

    for city in cities.values():
        if city.id == city_id:
            storage.delete(city)
            return {}, 200
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Creates an new City object and stores it
    """
    if request.headers.get("Content-Type") != "application/json":
        abort(400, "Not a JSON")
    states = storage.all(State)
    s = False

    for state in states.values():
        if state.id == state_id:
            s = True
    if not s:
        abort(404)
    fields = request.get_json()
    if not fields:
        return "Not a JSON", 400
    name = fields.get("name")
    if not name:
        return "Missing name", 400
    city = City(name=name, state_id=state_id)
    city.save()
    storage.save()
    return city.to_dict(), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    """
    Updates a city object
    """
    if request.headers.get("Content-Type") != "application/json":
        abort(400, "Not a JSON")
    for city in storage.all(City).values():
        if city.id == city_id:
            fields = request.get_json()
            if not fields:
                return "Not a JSON", 400
            for k, v in fields.items():
                if k == "name":
                    city.name = v
            city.save()
            storage.save()
            return city.to_dict(), 200
    abort(404)
