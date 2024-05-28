#!/usr/bin/python3
"""
This script defines CRUD routes for the link between Place and Amenity
objects
"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


storage_t = os.environ.get("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def amenities_in_place(place_id):
    """
    Retrieves a list of amenities of a Place object
    """
    places = storage.all(Place)
    amenities = []
    for place in places.values():
        if place.id == place_id:
            if storage_t == "db":
                for amenity in place.amenities:
                    amenities.append(amenity.to_dict())
                return amenities
            else:
                return place.amenity_ids
    abort(404)


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"]
)
def unlink_amenity(place_id, amenity_id):
    """
    Deletes an Amenity object or Amenity id from a place
    """
    places = storage.all(Place)
    for place in places.values():
        if place.id == place_id:
            if storage_t == "db":
                amenities = storage.all(Amenity)
                for amnty in amenities.values():
                    if amnty.id == amenity_id:
                        for amenity in place.amenities:
                            if amenity == amnty:
                                storage.delete(amnty)
                                return {}, 200
                        abort(404)
                abort(404)
            else:
                amenities = storage.all(Amenity)
                for amnty in amenities.values():
                    if amnty.id == amenity_id:
                        for amnty_id in place.amenity_ids:
                            if amenity_id == amnty_id:
                                place.amenity_ids.remove(amnty_id)
                                place.save()
                                storage.save()
                        abort(404)
                abort(404)
    abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def link_amnity(place_id, amenity_id):
    """
    Links amenity object to a place object
    """
    for place in storage.all(Place).values():
        if place.id == place_id:
            for amnty in storage.all(Amenity).values():
                if storage_t == "db":
                    if amnty.id == amenity_id:
                        for amenity in place.amenities:
                            if amnty == amenity:
                                return amenity.to_dict(), 200
                        place.amenities.append(amenity)
                        place.save()
                        storage.save()
                        return amenity.to_dict(), 201
                else:
                    if amnty.id == amenity_id:
                        for amnty_id in place.amenity_ids:
                            if amnty_id == amenity_id:
                                return amenity_id, 200
                        place.amenity_ids.append(amenity_id)
                        place.save()
                        storage.save()
                        return amenity_id, 201
            abort(404)
    abort(404)
