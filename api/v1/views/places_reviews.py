#!/usr/bin/python3
"""
Handles all default RestFul API actions for place reviews
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    places = storage.all(Place)
    place_key = "Place." + place_id

    if place_key not in places:
        abort(404)

    place = places[place_key]
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    reviews = storage.all(Review)
    review_key = "Review." + review_id

    if review_key not in reviews:
        abort(404)

    review = reviews[review_key]
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    reviews = storage.all(Review)
    review_key = "Review." + review_id

    if review_key in reviews:
        storage.delete(reviews[review_key])
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    places = storage.all(Place)
    place_key = "Place." + place_id

    if place_key not in places:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    body_request = request.get_json()
    if 'user_id' not in body_request:
        abort(400, "Missing user_id")

    users = storage.all(User)
    user_key = "User." + body_request['user_id']

    if user_key not in users:
        abort(404)

    if 'text' not in body_request:
        abort(400, "Missing text")

    body_request['place_id'] = place_id
    new_review = Review(**body_request)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    reviews = storage.all(Review)
    review_key = "Review." + review_id

    if review_key in reviews:
        review = reviews[review_key]

        if not request.is_json:
            abort(400, "Not a JSON")

        body_request = request.get_json()
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in body_request.items():
            if key not in ignore:
                setattr(review, key, value)

        storage.save()
        return jsonify(review.to_dict()), 200

    abort(404)
