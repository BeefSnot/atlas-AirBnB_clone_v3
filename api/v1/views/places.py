#!/usr/bin/python3
"""
places module that handles all default RESTful API
actions.
"""
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'], strict_slashes=False)
def place_all(city_id):
    """Returns all places for a specific city ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """Returns a place by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'], strict_slashes=False)
def place_delete(place_id):
    """Deletes a place by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Adds a place using POST"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()

    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a place using PUT"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()
    not_these = ["id", "created_at", "updated_at", "city_id", "user_id"]
    for key, value in data.items():
        if key not in not_these:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
