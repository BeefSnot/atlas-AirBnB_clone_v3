#!/usr/bin/python3
"""
Handles app_views for Review class
"""
from models.review import Review
from models.city import City
from models.user import User
from models.review import Review
from models.place import Place
from flask import jsonify, abort, request
from api.v1.views import app_views, storage


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_post_reviews(place_id):
    """returns json list of all reviews in storage or returns new review"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place:
            reviews = [review.to_dict() for review in place.reviews]
            return jsonify(reviews)
        else:
            abort(404)
    elif request.method == 'POST':
        place = storage.get(Place, place_id)
        if place:
            if request.is_json:
                req = request.get_json()
                user_id = req.get('user_id')
                text = req.get('text')
                if user_id:
                    user = storage.get(User, user_id)
                    if user:
                        if text:
                            new_review = Review(**req)
                            new_review.place_id = place_id
                            new_review.save()
                            return jsonify(new_review.to_dict()), 201
                        else:
                            abort(400, description='Missing text')
                    else:
                        abort(404)
                else:
                    abort(400, description='Missing user_id')
            else:
                abort(400, description='Not a JSON')
        else:
            abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review_id(review_id):
    """retrieves, deletes, or updates json'd review object"""
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
        else:
            abort(404)
    elif request.method == 'DELETE':
        review = storage.get(Review, review_id)
        if review:
            storage.delete(review)
            return jsonify({}), 200
        else:
            abort(404)
    elif request.method == 'PUT':
        review = storage.get(Review, review_id)
        if review:
            if request.is_json:
                update_dict = request.get_json()
                update_dict = {key: value for key, value
                               in update_dict.items() if key not in
                               ['id', 'user_id', 'place_id',
                                'created_at', 'updated_at']}
                for key, value in update_dict.items():
                    setattr(review, key, value)
                review.save()
                return jsonify(review.to_dict()), 200
            else:
                abort(400, description='Not a JSON')
        else:
            abort(404)
