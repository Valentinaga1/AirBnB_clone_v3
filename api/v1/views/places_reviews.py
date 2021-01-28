#!/usr/bin/python3
"""
starting the routes for places_reviews and methods GET, POST, PUT, DELETE
"""
from flask import Flask, Blueprint, jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """Show a review of a place"""
    reviews_list = []
    places_to_search = storage.get(Place, place_id)
    if places_to_search is None:
        abort(404)
    for review in places_to_search.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """Show one review by specific id"""
    review_to_search = storage.get(Review, review_id)
    if review_to_search is None:
        abort(404)
    return jsonify(review_to_search.to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """Delete one review"""
    review_to_search = storage.get(Review, review_id)
    if review_to_search is None:
        abort(404)
    storage.delete(review_to_search)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """ create a review of an specific place id"""
    places_to_search = storage.get(Place, place_id)
    print(places_to_search)
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
    if 'text' not in post_data:
        abort(400, "Missing text")
    post_data["place_id"] = place_id
    new_instance_review = Review(**post_data)
    new_instance_review.save()
    return (jsonify(new_instance_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """ update a review for an specific id"""
    review_to_search = storage.get(Review, review_id)
    print(review_to_search)
    print("hello")
    if review_to_search is None:
        abort(404)
    post_data = request.get_json()
    print(post_data)
    if post_data is None:
        abort(400, "Not a JSON")
    for key, value in post_data.items():
        if key != "id" and key != "user_id" and key != "user_id"\
           and key != "created_at" and key != "updated_at":
            setattr(review_to_search, key, value)
    review_to_search.save()
    return (jsonify(review_to_search.to_dict()), 200)
