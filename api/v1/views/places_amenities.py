#!/usr/bin/python3
"""
Handle API request for the relationship between Place and Amenity
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities_by_place(place_id):
    places = storage.all(Place)
    place_key = "Place." + place_id

    if place_key not in places:
        abort(404)

    place = places[place_key]
    amenity_list = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenity_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    places = storage.all(Place)
    amenities = storage.all(Amenity)
    place_key = "Place." + place_id
    amenity_key = "Amenity." + amenity_id

    if place_key not in places or amenity_key not in amenities:
        abort(404)

    place = places[place_key]
    amenity = amenities[amenity_key]

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    places = storage.all(Place)
    amenities = storage.all(Amenity)
    place_key = "Place." + place_id
    amenity_key = "Amenity." + amenity_id

    if place_key not in places or amenity_key not in amenities:
        abort(404)

    place = places[place_key]
    amenity = amenities[amenity_key]

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
