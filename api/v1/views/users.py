#!/usr/bin/python3
"""
Handle API actions related to User objects
"""

from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    users = storage.all(User)
    user_key = "User." + user_id

    if user_key not in users:
        abort(404)

    return jsonify(users[user_key].to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    users = storage.all(User)
    user_key = "User." + user_id

    if user_key in users:
        storage.delete(users[user_key])
        storage.save()
        return jsonify({}), 200

    abort(404)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    if not request.is_json:
        abort(400, "Not a JSON")

    body_request = request.get_json()
    if 'email' not in body_request:
        abort(400, "Missing email")
    if 'password' not in body_request:
        abort(400, "Missing password")

    new_user = User(**body_request)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    users = storage.all(User)
    user_key = "User." + user_id

    if user_key in users:
        user = users[user_key]

        if not request.is_json:
            abort(400, "Not a JSON")

        body_request = request.get_json()
        for key, value in body_request.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict()), 200

    abort(404)
