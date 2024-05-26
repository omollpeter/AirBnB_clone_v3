#!/usr/bin/python3
"""
This script handles all requests for state object
"""


from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route("/states", strict_slashes=False, methods=["GET"])
def states():
    """
    Retrieves a list of all State objects
    """
    states = storage.all(State)

    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return states_list


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def state(state_id):
    """
    Retrieves a specific state using its id
    """
    states = storage.all(State)

    for state in states.values():
        if state.id == state_id:
            return state.to_dict()
    abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Deletes a specific state from the states objects
    """
    states = storage.all(State)

    for state in states.values():
        if state.id == state_id:
            storage.delete(state)
            return {}, 200
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """
    Creates an new State object and stores it
    """
    fields = request.get_json()
    if not fields:
        abort(400, "Not a JSON")
    name = fields.get("name")
    if not name:
        abort(400, "Missing name")
    state = State(name=name)
    state.save()
    storage.save()
    return state.to_dict(), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """
    Updates a state object
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            fields = request.get_json()
            if not fields:
                abort(400, "Not a JSON")
            for k, v in fields.items():
                if k == "name":
                    state.name = v
            state.save()
            storage.save()
            return state.to_dict(), 200
    abort(404)
