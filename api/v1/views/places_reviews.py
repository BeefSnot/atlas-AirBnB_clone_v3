#!/usr/bin/python3
"""
Handles app_views for Review class
"""
from models.review import Review
from models.user import User
from models.place import Place
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'], strict_slashes=False)
def get_post_reviews(place_id):
    """Returns a list of all reviews for a place or creates a new review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        if not request.is_json:
            abort(400, description='Not a JSON')
        req = request.get_json()
        user_id = req.get('user_id')
        text = req.get('text')
        if not user_id:
            abort(400, description='Missing user_id')
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        if not text:
            abort(400, description='Missing text')
        new_review = Review(**req)
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def get_delete_update_review(review_id):
    """Retrieves, deletes, or updates a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            abort(400, description='Not a JSON')
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
