#!/usr/bin/python3
"""
This module creates the view for all state objects
and handles all default api actions
"""

from api.v1.views import app_views, index
from flask import Flask, abort, jsonify, request
from models import storage
from models.user import User
from models.amenity import Amenity


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    This method retrieves a list of all state objects
    Args: users - list of all users, keys excluded
          users_json - all users converted to a list of dictionaries
    Return: a json dictionary containing all user objects
    """
    users = storage.all(User).values()
    users_json = [user.to_dict() for user in users]
    return jsonify(users_json)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    This method retrieves one user object
    Args: user - retrieves one user object, based on its user id
          user_json - user object converted to a dictionary
    Return: a json dictionary containing one user object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)  # Bad request
    user_json = user.to_dict()
    return jsonify(user_json)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    This method deletes one user object
    Args: user - retrieves one user object, based on its user id
    Return: an empty json dictionary
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)  # Bad request
    storage.delete(user)
    print(f"type of user: {type(user)}")
    storage.save()
    return jsonify({}), 200  # OK


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    This method creates a user object
    Args: user - gets an HTTP body request to a user object
          json_data - holds the json data request
          user_json - holds the dictionary of a user object
    Return: a json dictionary containing one user object
    """
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")
    if "email" not in json_data:
        abort(400, "Missing email")
    if "password" not in json_data:
        abort(400, "Missing password")
    user = User(**json_data)
    storage.new(user)
    storage.save()
    user_json = user.to_dict()
    return jsonify(user_json), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    This method updates a user object
    Args: user - retrieves one user object, based on its user id
          json_data - json request data for readability
          user_json - user object converted to a dictionary
    Return: a json dictionary
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)  # Bad request
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")  # Bad request
    leave_out_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in json_data.items():
        if key not in leave_out_keys:
            setattr(user, key, value)
    storage.save()
    user_json = user.to_dict()
    return jsonify(user_json), 200  # OK


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    This method retrieves a list of all amenity objects
    Args: amenities - list of all amenities, keys excluded
          amenities_json - all amenities converted to a list of dictionaries
    Return: a json dictionary containing all amenity objects
    """
    amenities = storage.all(Amenity).values()
    amenities_json = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_json)


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """
    This method retrieves one amenity object
    Args: amenity - retrieves one amenity object, based on its amenity id
          amenity_json - amenity object converted to a dictionary
    Return: a json dictionary containing one amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)  # Bad request
    amenity_json = amenity.to_dict()
    return jsonify(amenity_json)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    This method deletes one amenity object
    Args: amenity - retrieves one amenity object, based on its amenity id
    Return: an empty json dictionary
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)  # Bad request
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200  # OK


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    This method creates an amenity object
    Args: amenity - gets an HTTP body request to an amenity object
          json_data - holds the json data request
          amenity_json - holds the dictionary of an amenity object
    Return: a json dictionary containing one amenity object
    """
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")
    amenity = Amenity(**json_data)
    storage.new(amenity)
    storage.save()
    amenity_json = amenity.to_dict()
    return jsonify(amenity_json), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    This method updates an amenity object
    Args: amenity - retrieves one amenity object, based on its amenity id
          json_data - json request data for readability
          amenity_json - amenity object converted to a dictionary
    Return: a json dictionary
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)  # Bad request
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, "Not a JSON")  # Bad request
    leave_out_keys = ["id", "created_at", "updated_at"]
    for key, value in json_data.items():
        if key not in leave_out_keys:
            setattr(amenity, key, value)
    storage.save()
    amenity_json = amenity.to_dict()
    return jsonify(amenity_json), 200  # OK
