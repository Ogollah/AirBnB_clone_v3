#!/usr/bin/python3
"""
Handles all default RESTful API actions for Amenity
"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    amenities = storage.all(Amenity)
    amenity_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    amenities = storage.all(Amenity)
    amenity_key = "Amenity." + amenity_id

    if amenity_key not in amenities:
        abort(404)

    return jsonify(amenities[amenity_key].to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    amenities = storage.all(Amenity)
    amenity_key = "Amenity." + amenity_id

    if amenity_key in amenities:
        storage.delete(amenities[amenity_key])
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    if not request.is_json:
        abort(400, "Not a JSON")

    body_request = request.get_json()
    if 'name' not in body_request:
        abort(400, "Missing name")

    new_amenity = Amenity(**body_request)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    amenities = storage.all(Amenity)
    amenity_key = "Amenity." + amenity_id

    if amenity_key in amenities:
        amenity = amenities[amenity_key]

        if not request.is_json:
            abort(400, "Not a JSON")

        body_request = request.get_json()
        for key, value in body_request.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)

        storage.save()
        return jsonify(amenity.to_dict()), 200

    abort(404)
