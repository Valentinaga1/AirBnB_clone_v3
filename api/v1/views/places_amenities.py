#!/usr/bin/python3
"""
starting the routes for places_reviews and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models import storage_t
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=["GET"])
def get_amenities_relation(place_id):
    """Show a review of a place"""
    amenities_list = []
    places_to_search = storage.get(Place, place_id)
    if places_to_search is None:
        abort(404)
    if storage_t == 'db':
        for amenitie in places_to_search.amenities:
            amenities_list.append(amenitie.to_dict())
        return jsonify(amenities_list)
    else:
        for amenitie in places_to_search.amenity_ids:
            amenities_list.append(amenitie.to_dict())
        return jsonify(amenities_list)

@app_views.route("/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_amenities_relation(place_id, amenity_id):
    """Delete one review"""
    places_to_search = storage.get(Place, place_id)
    if places_to_search is None:
        abort(404)
    amenities_to_search = storage.get(Amenity, amenity_id)
    if amenities_to_search is None:
        abort(404)
    if storage_t == 'db':
        amenity_place_asig = places_to_search.amenities
        if amenities_to_search not in amenity_place_asig:
            abort(404)
        else:
            amenity_place_asig.remove(amenities_to_search)
            places_to_search.save()
            return jsonify({}), 200
    else:
        amenity_place_asig = places_to_search.amenity_ids
        if amenities_to_search in amenity_place_asig:
            abort(404)
        else:
            amenity_place_asig.remove(amenity_id)
            places_to_search.save()
            return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=["POST"])
def create_amenities_relation(place_id, amenity_id):
    """ create a review of an specific place id"""
    places_to_search = storage.get(Place, place_id)
    amenities_to_search = storage.get(Amenity, amenity_id)
    # print(places_to_search)
    # print(amenities_to_search)
    if places_to_search is None or amenities_to_search is None:
        abort(404)
    if storage_t == 'db':
        amenity_place_asig = places_to_search.amenities
        if amenities_to_search in amenity_place_asig:
            return jsonify(amenities_to_search.to_dict()), 200
        else:
            amenity_place_asig.append(amenities_to_search)
            places_to_search.save()
            return jsonify(amenities_to_search.to_dict()), 201
    else:
        amenity_place_asig = places_to_search.amenity_ids
        if amenities_to_search in amenity_place_asig:
            return amenity_id, 200
        else:
            amenity_place_asig.append(amenity_id)
            places_to_search.save()
            return amenity_id, 201
