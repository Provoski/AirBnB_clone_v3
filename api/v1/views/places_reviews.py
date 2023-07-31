#!/usr/bin/python3
"""place_reviews module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route(
                    '/places/<string:place_id>/reviews',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_place_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route(
                    '/reviews/<string:review_id>',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
                    '/reviews/<string:review_id>',
                    methods=['DELETE'],
                    strict_slashes=False
                    )
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                    '/places/<string:place_id>/reviews',
                    methods=['POST'],
                    strict_slashes=False
                    )
def create_place_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = storage.get(User, data['user_id'])
    if not user_id:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
                    '/reviews/<string:review_id>',
                    methods=['PUT'],
                    strict_slashes=False
                    )
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
