#!/usr/bin/python3
"""
Handles app_views for Amenity class
"""
from models.amenity import Amenity
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Returns a list of all amenities in storage"""
    amenities = [amen.to_dict() for amen in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    if not request.is_json:
        abort(400, description='Not a JSON')
    req = request.get_json()
    name = req.get('name')
    if not name:
        abort(400, description='Missing name')
    new_amen = Amenity(**req)
    new_amen.save()
    return jsonify(new_amen.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    req = request.get_json()
    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
