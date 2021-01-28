#!/usr/bin/python3
"""
starting the routes for cities and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_cities(state_id):
    """Show cities of state"""
    cities_list = []
    state_to_search = storage.get(State, state_id)
    if state_to_search is None:
        abort(404)
    for city in state_to_search.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", strict_slashes=False,
                 methods=["GET"])
def get_city(city_id):
    """Show one city by specific id"""
    city_to_search = storage.get(City, city_id)
    if city_to_search is None:
        abort(404)
    return jsonify(city_to_search.to_dict())


@app_views.route("cities/<city_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_citie(city_id):
    """Delete one citie"""
    citie_to_search = storage.get(City, city_id)
    if citie_to_search is None:
        abort(404)
    storage.delete(citie_to_search)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities/",
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):
    """ create a city by an specific state id"""
    state_to_search = storage.get(State, state_id)
    print(state_to_search)
    if state_to_search is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    if 'name' not in post_data:
        abort(400, "Missing name")
    post_data["state_id"] = state_to_search.id
    new_instance_city = City(**post_data)
    new_instance_city.save()
    return (jsonify(new_instance_city.to_dict()), 201)


@app_views.route("cities/<city_id>", strict_slashes=False,
                 methods=["PUT"])
def update_city(city_id):
    """ update a City for an specific id"""
    city_to_search = storage.get(City, city_id)
    if city_to_search is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        abort(400, "Not a JSON")
    for key, value in post_data.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(city_to_search, key, value)
    city_to_search.save()
    return (jsonify(city_to_search.to_dict()), 200)
