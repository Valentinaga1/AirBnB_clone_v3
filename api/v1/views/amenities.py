#!/usr/bin/python3
"""
starting the routes for amenities and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/amenities/", strict_slashes=False, methods=["GET"])
def get_amenities():
    """Show all amenities"""
    amenities_list = []
    for amenity in storage.all(Amenity).values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def get_amenity(amenity_id):
    """Show one amenity"""
    amenity_to_search = storage.get(Amenity, amenity_id)
    if amenity_to_search is None:
        abort(404)
    return jsonify(amenity_to_search.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete one amenity"""
    amenity_to_search = storage.get(Amenity, amenity_id)
    if amenity_to_search is None:
        abort(404)
    storage.delete(amenity_to_search)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/",
                 strict_slashes=False, methods=["POST"])
def create_amenities():
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if 'name' not in post_data:
        abort(400, "Missing name")
    new_instance_amenity = Amenity(**post_data)
    new_instance_amenity.save()
    return (jsonify(new_instance_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """ update amenities for an specific id"""
    amenity_to_search = storage.get(Amenity, amenity_id)
    if amenity_to_search is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    for key, value in post_data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(amenity_to_search, key, value)
    amenity_to_search.save()
    return (jsonify(amenity_to_search.to_dict()), 200)
