#!/usr/bin/python3
"""
Handles app_views for Place class
"""
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_post_places(city_id):
    """returns json list of all places in storage or returns new place"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city:
            places = [place.to_dict() for place in city.places]
            return jsonify(places)
        else:
            abort(404)
    elif request.method == 'POST':
        city = storage.get(City, city_id)
        if city:
            if request.is_json:
                req = request.get_json()
                user_id = req.get('user_id')
                name = req.get('name')
                if user_id:
                    user = storage.get(User, user_id)
                    if user:
                        if name:
                            new_place = Place(**req)
                            new_place.city_id = city_id
                            new_place.save()
                            return jsonify(new_place.to_dict()), 201
                        else:
                            abort(400, description='Missing name')
                    else:
                        abort(404)
                else:
                    abort(400, description='Missing user_id')
            else:
                abort(400, description='Not a JSON')
        else:
            abort(404)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_place_id(place_id):
    """retrieves, deletes, or updates json'd place object"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place:
            return jsonify(place.to_dict())
        else:
            abort(404)
    elif request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place:
            storage.delete(place)
            return jsonify({}), 200
        else:
            abort(404)
    elif request.method == 'PUT':
        place = storage.get(Place, place_id)
        if place:
            if request.is_json:
                update_dict = request.get_json()
                update_dict = {key: value for key, value
                               in update_dict.items() if key not in
                               ['id', 'user_id', 'city_id',
                                'created_at', 'updated_at']}
                for key, value in update_dict.items():
                    setattr(place, key, value)
                place.save()
                return jsonify(place.to_dict()), 200
            else:
                abort(400, description='Not a JSON')
        else:
            abort(404)
