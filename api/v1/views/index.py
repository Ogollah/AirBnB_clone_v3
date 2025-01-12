#!/usr/bin/python3
"""
Define routes blueprints
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return application status.
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Count storage objects.
    """
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    json_stats = {}

    for name, cls in classes.items():
        json_stats.update({name: storage.count(cls)})

    return jsonify(json_stats)
