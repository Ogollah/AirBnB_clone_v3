#!/usr/bin/python3
"""
View to handle API actions related to Place objects
"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    cities = storage.all(City)
    city_key = "City." + city_id

    if city_key not in cities:
        abort(404)

    city = cities[city_key]
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    places = storage.all(Place)
    place_key = "Place." + place_id

    if place_key not in places:
        abort(404)

    place = places[place_key]
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    places = storage.all(Place)
    place_key = "Place." + place_id

    if place_key in places:
        storage.delete(places[place_key])
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    cities = storage.all(City)
    city_key = "City." + city_id

    if city_key not in cities:
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

    if 'name' not in body_request:
        abort(400, "Missing name")

    body_request['city_id'] = city_id
    new_place = Place(**body_request)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    places = storage.all(Place)
    place_key = "Place." + place_id

    if place_key in places:
        place = places[place_key]

        if not request.is_json:
            abort(400, "Not a JSON")

        body_request = request.get_json()
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in body_request.items():
            if key not in ignore:
                setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict()), 200

    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Search for Place objects based on JSON request criteria
    """
    if not request.is_json:
        abort(400, "Not a JSON")

    search_criteria = request.get_json()
    states = search_criteria.get("states", [])
    cities = search_criteria.get("cities", [])
    amenities = search_criteria.get("amenities", [])

    places_result = []

    if not states and not cities and not amenities:
        places_result = [place.to_dict() for place in storage.all(Place).values()]
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        if city.id not in cities:
                            cities.append(city.id)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if all(amenity in place.amenities_ids for amenity in amenities):
                        places_result.append(place.to_dict())

    return jsonify(places_result)
