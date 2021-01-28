#!/usr/bin/python3
"""
starting the routes for states and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states/", strict_slashes=False, methods=["GET"])
def get_states():
    """Show all states"""
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state(state_id):
    """Show one state"""
    state_to_search = storage.get(State, state_id)
    if state_to_search is None:
        abort(404)
    return jsonify(state_to_search.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id):
    """Delete one state"""
    state_to_search = storage.get(State, state_id)
    if state_to_search is None:
        abort(404)
    storage.delete(state_to_search)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", strict_slashes=False, methods=["POST"])
def create_states():
    """
    create a new state using method POST
    """
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if 'name' not in post_data:
        abort(400, "Missing name")
    new_instance_state = State(**post_data)
    new_instance_state.save()
    return (jsonify(new_instance_state.to_dict()), 201)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """ update states for an specific id"""
    state_to_search = storage.get(State, state_id)
    if state_to_search is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    for key, value in post_data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(state_to_search, key, value)
    state_to_search.save()
    return (jsonify(state_to_search.to_dict()), 200)
