#!/usr/bin/python3
"""
This script defines CRUD routes for Review objects
"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_reviews(place_id):
    """
    Retrieves all the reviews a place
    """
    places = storage.all(Place)
    reviews_list = []
    for place in places.values():
        if place.id == place_id:
            for review in place.reviews:
                reviews_list.append(review.to_dict())
            return reviews_list
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def review(review_id):
    """
    Retrieves a Review object based on its id
    """
    reviews = storage.all(Review)
    for review in reviews.values():
        if review.id == review_id:
            return review.to_dict()
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Deletes a Review object
    """
    reviews = storage.all(Review)
    for review in reviews.values():
        if review.id == review_id:
            storage.delete(review)
            return {}, 200
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_place_review(place_id):
    """
    Creates a Review object for a place
    """
    places = storage.all(Place)
    fields = request.get_json()

    p = False
    for place in places.values():
        if place.id == place_id:
            p = True
    if not p:
        abort(404)
    if not fields:
        abort(400, "Not a JSON")
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
    text = fields.get("text")
    if not text:
        abort(400, "Missing text")
    fields["place_id"] = place_id
    review = Review(**fields)
    review.save()
    storage.save()
    return review.to_dict(), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """
    Updates a Review object
    """
    for review in storage.all(Review).values():
        if review.id == review_id:
            fields = request.get_json()
            if not fields:
                abort(400, "Not a JSON")
            for k, v in fields.items():
                if k == "text":
                    review.text = v
            review.save()
            storage.save()
            return review.to_dict(), 200
    abort(404)
