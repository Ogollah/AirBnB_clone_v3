#!/usr/bin/python3
"""
Handles all default RESTful API actions for states
"""

from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_states(state_id=None):
    """
    Handles states objects using state_id
    """
    states = storage.all(State)

    if request.method == 'GET':
        return get_states(state_id, states)

    elif request.method == 'DELETE':
        return delete_state(state_id, states)

    elif request.method == 'POST':
        return create_state(request, states)

    elif request.method == 'PUT':
        return update_state(state_id, request, states)

    else:
        abort(501)


def get_states(state_id, states):
    if not state_id:
        return jsonify([state.to_dict() for state in states.values()])
    else:
        return jsonify(get_state_by_id(state_id, states))


def get_state_by_id(state_id, states):
    key = 'State.' + state_id
    if key in states:
        return states[key].to_dict()
    abort(404)


def delete_state(state_id, states):
    key = 'State.' + state_id
    if key in states:
        storage.delete(states[key])
        storage.save()
        return jsonify({}), 200
    abort(404)


def create_state(request, states):
    if not request.is_json:
        abort(400, 'Not a JSON')

    body_request = request.get_json()
    if 'name' not in body_request:
        abort(400, 'Missing name')

    new_state = State(**body_request)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


def update_state(state_id, request, states):
    key = 'State.' + state_id
    if key in states:
        state = states[key]

        if not request.is_json:
            abort(400, 'Not a JSON')

        body_request = request.get_json()
        for key, val in body_request.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)

        storage.save()
        return jsonify(state.to_dict()), 200
    abort(404)
