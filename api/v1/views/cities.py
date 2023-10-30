#!/usr/bin/python3
"""
City objects that handle all default RESTful API actions
"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    state_key = "State." + state_id
    states = storage.all(State)

    if state_key not in states:
        abort(404)

    state = states[state_key]
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    cities = storage.all(City)
    city_key = "City." + city_id

    if city_key not in cities:
        abort(404)

    return jsonify(cities[city_key].to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    cities = storage.all(City)
    city_key = "City." + city_id

    if city_key in cities:
        storage.delete(cities[city_key])
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state_key = "State." + state_id
    states = storage.all(State)

    if state_key not in states:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    body_request = request.get_json()
    if 'name' not in body_request:
        abort(400, "Missing name")

    body_request["state_id"] = state_id
    new_city = City(**body_request)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    cities = storage.all(City)
    city_key = "City." + city_id

    if city_key in cities:
        city = cities[city_key]

        if not request.is_json:
            abort(400, "Not a JSON")

        body_request = request.get_json()
        for key, value in body_request.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)

        storage.save()
        return jsonify(city.to_dict()), 200

    abort(404)
