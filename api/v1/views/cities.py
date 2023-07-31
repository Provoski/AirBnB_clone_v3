#!/usr/bin/python3
"""cities module"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route(
                    '/states/<string:state_id>/cities',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route(
                    '/cities/<string:city_id>',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
                    '/cities/<string:city_id>',
                    methods=['DELETE'],
                    strict_slashes=False
                    )
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(
                    '/states/<string:state_id>/cities',
                    methods=['POST'],
                    strict_slashes=False
                    )
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route(
                    '/cities/<string:city_id>',
                    methods=['PUT'],
                    strict_slashes=False
                    )
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
