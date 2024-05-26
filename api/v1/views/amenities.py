#!/usr/bin/python3
"""
This script handles all requests for amenity object
"""


from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
def amenities():
    """
    Retrieves a list of all Amenity objects
    """
    amenities = storage.all(Amenity)

    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return amenities_list


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def amenity(amenity_id):
    """
    Retrieves a specific amenity using its id
    """
    amenities = storage.all(Amenity)

    for amenity in amenities.values():
        if amenity.id == amenity_id:
            return amenity.to_dict()
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes a specific amenity from the amenities objects
    """
    amenities = storage.all(Amenity)

    for amenity in amenities.values():
        if amenity.id == amenity_id:
            storage.delete(amenity)
            return {}, 200
    abort(404)


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """
    Creates an new Amenity object and stores it
    """
    fields = request.get_json()
    if not fields:
        return "Not a JSON", 400
    name = fields.get("name")
    if not name:
        return "Missing name", 400
    amenity = Amenity(name=name)
    amenity.save()
    storage.save()
    return amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """
    Updates a amenity object
    """
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            fields = request.get_json()
            if not fields:
                return "Not a JSON", 400
            for k, v in fields.items():
                if k == "name":
                    amenity.name = v
            amenity.save()
            storage.save()
            return amenity.to_dict(), 200
    abort(404)
