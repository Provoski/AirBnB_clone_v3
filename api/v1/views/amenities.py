#!/usr/bin/python3
"""amenities odule"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity():
    amenity_list = []
    amenities = storage.all(Amenity)
    for key, amenity in amenities.items():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list), 200


@app_views.route(
                    '/amenities/<string:amenity_id>',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    return abort(404)


@app_views.route(
                    '/amenities/<string:amenity_id>',
                    methods=['DELETE'],
                    strict_slashes=False
                    )
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return {}, 200
    return abort(404)


@app_views.route(
                    '/amenities',
                    methods=['POST'],
                    strict_slashes=False
                    )
def create_amenity():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON' if not data else 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
                    '/amenities/<string:amenity_id>',
                    methods=['PUT'],
                    strict_slashes=False
                    )
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    return abort(404)
