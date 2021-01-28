#!/usr/bin/python3
"""
starting the routes for places and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """Show place of a city"""
    places_list = []
    cities_to_search = storage.get(City, city_id)
    if cities_to_search is None:
        abort(404)
    for place in cities_to_search.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """Show one place by specific id"""
    places_to_search = storage.get(Place, place_id)
    if places_to_search is None:
        abort(404)
    return jsonify(places_to_search.to_dict())


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_place(city_id):
    """Delete one place"""
    places_to_search = storage.get(Place, city_id)
    if places_to_search is None:
        abort(404)
    storage.delete(places_to_search)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """ create a citplacey by an specific city id"""
    places_to_search = storage.get(City, city_id)
    if places_to_search is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    user_verif = storage.get(User, post_data.get("user_id"))
    if 'user_id' not in post_data:
        abort(400, "Missing user_id")
    if user_verif is None:
        abort(404)
    if 'name' not in post_data:
        abort(400, "Missing name")
    post_data["city_id"] = city_id
    new_instance_place = Place(**post_data)
    new_instance_place.save()
    return (jsonify(new_instance_place.to_dict()), 201)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["PUT"])
def update_place(city_id):
    """ update a place for an specific id"""
    places_to_search = storage.get(Place, city_id)
    if places_to_search is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    for key, value in post_data.items():
        if key != "id" and key != "city_id" and key != "user_id"\
           and key != "created_at" and key != "updated_at":
            setattr(places_to_search, key, value)
    city_to_search.save()
    return (jsonify(places_to_search.to_dict()), 200)
