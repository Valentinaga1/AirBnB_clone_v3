#!/usr/bin/python3
"""
starting the routes for users and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users/", strict_slashes=False, methods=["GET"])
def get_users():
    """Show all users"""
    users_list = []
    for user in storage.all(User).values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    """Show one user"""
    user_to_search = storage.get(User, user_id)
    if user_to_search is None:
        abort(404)
    return jsonify(user_to_search.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    """Delete one user"""
    user_to_search = storage.get(User, user_id)
    if user_to_search is None:
        abort(404)
    storage.delete(user_to_search)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", strict_slashes=False, methods=["POST"])
def create_users():
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if 'email' not in post_data:
        abort(400, "Missing email")
    if 'password' not in post_data:
        abort(400, "Missing password")
    new_instance_user = User(**post_data)
    new_instance_user.save()
    return (jsonify(new_instance_user.to_dict()), 201)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """ update users for an specific id"""
    user_to_search = storage.get(User, user_id)
    if user_to_search is None:
        abort(404)
    post_data = request.get_json()
    # {name : value}
    if post_data is None:
        abort(400, "Not a JSON")
    for key, value in post_data.items():
        if key != "id" and key != "email" and key != "created_at"\
           and key != "updated_at":
            setattr(user_to_search, key, value)
    user_to_search.save()
    return (jsonify(user_to_search.to_dict()), 200)
