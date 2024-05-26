#!/usr/bin/python3
"""
This script handles all requests for user object
"""


from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def users():
    """
    Retrieves a list of all User objects
    """
    users = storage.all(User)

    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return users_list


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def user(user_id):
    """
    Retrieves a specific user using its id
    """
    users = storage.all(User)

    for user in users.values():
        if user.id == user_id:
            return user.to_dict()
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a specific user from the users objects
    """
    users = storage.all(User)

    for user in users.values():
        if user.id == user_id:
            storage.delete(user)
            return {}, 200
    abort(404)


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """
    Creates an new User object and stores it
    """
    fields = request.get_json()
    if not fields:
        return "Not a JSON", 400
    first_name = fields.get("first_name")
    last_name = fields.get("last_name")
    email = fields.get("email")
    password = fields.get("password")
    if not email:
        return "Missing email", 400
    if not password:
        return "Missing password", 400
    user = User(**fields)
    user.save()
    storage.save()
    return user.to_dict(), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """
    Updates a user object
    """
    for user in storage.all(User).values():
        if user.id == user_id:
            fields = request.get_json()
            if not fields:
                return "Not a JSON", 400
            for k, v in fields.items():
                if k == "first_name":
                    user.first_name = v
                if k == "last_name":
                    user.last_name = v
                if k == "password":
                    user.password = v
            user.save()
            storage.save()
            return user.to_dict(), 200
    abort(404)
