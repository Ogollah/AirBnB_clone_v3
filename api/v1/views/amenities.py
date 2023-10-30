#!/usr/bin/python3
"""
Handles all default RESTful API actions for Amenity
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_amenity(amenity_id=None):
    """
    Handles amenity objects using amenity id
    """
    amenities = storage.all(Amenity)

    if request.method == 'GET':
        if not amenity_id:
            return get_all_amenities(amenities)
        return get_amenity(amenity_id, amenities)

    elif request.method == 'DELETE':
        return delete_amenity(amenity_id, amenities)

    elif request.method == 'POST':
        return create_amenity(request)

    elif request.method == 'PUT':
        return update_amenity(amenity_id, request, amenities)

    else:
        abort(501)


def get_all_amenities(amenities):
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


def get_amenity(amenity_id, amenities):
    key = 'Amenity.' + amenity_id
    if key in amenities:
        return jsonify(amenities[key].to_dict())
    abort(404)


def delete_amenity(amenity_id, amenities):
    key = 'Amenity.' + amenity_id
    if key in amenities:
        storage.delete(amenities[key])
        storage.save()
        return jsonify({}), 200
    abort(404)


def create_amenity(request):
    if not request.is_json:
        abort(400, 'Not a JSON')

    body_request = request.get_json()
    if 'name' not in body_request:
        abort(400, 'Missing name')

    new_amenity = Amenity(**body_request)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


def update_amenity(amenity_id, request, amenities):
    key = 'Amenity.' + amenity_id
    if key in amenities:
        amenity = amenities[key]

        if not request.is_json:
            abort(400, 'Not a JSON')

        body_request = request.get_json()
        for key, val in body_request.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, val)

        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
