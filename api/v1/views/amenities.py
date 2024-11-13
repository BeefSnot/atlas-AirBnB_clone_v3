#!/usr/bin/python3
"""
Handles app_views for Amenity class
"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_post_amenities():
    """returns json list of all amenities in storage or returns new amenity"""
    if request.method == 'GET':
        amens = []
        for amen in storage.all(Amenity).values():
            amens.append(amen.to_dict())
        return jsonify(amens)
    elif request.method == 'POST':
        if request.is_json:
            req = request.get_json()
            name = req.get('name')
            if name:
                new_amen = Amenity(**req)
                new_amen.save()
                return jsonify(new_amen.to_dict()), 201
            else:
                abort(400, description='Missing name')
        else:
            abort(400, description='Not a JSON')


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """retrieves, deletes, or updates json'd amenity object"""
    if request.method == 'GET':
        amen = storage.get(Amenity, amenity_id)
        if amen:
            return jsonify(amen.to_dict())
        else:
            abort(404)
    elif request.method == 'DELETE':
        amen = storage.get(Amenity, amenity_id)
        if amen:
            storage.delete(amen)
            return {}, 200
        else:
            abort(404)
    elif request.method == 'PUT':
        amen = storage.get(Amenity, amenity_id)
        if amen:
            if request.is_json:
                update_dict = request.get_json()
                update_dict = {key: value for key, value
                               in update_dict.items() if key not in
                               ['id', 'created_at', 'updated_at']}
                for key, value in update_dict.items():
                    setattr(amen, key, value)
                amen.save()
                return jsonify(amen.to_dict()), 200
            else:
                abort(400, description='Not a JSON')
        else:
            abort(404)
