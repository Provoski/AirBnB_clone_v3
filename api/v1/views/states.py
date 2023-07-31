#!/usr/bin/python3
"""states module"""
from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route(
                    '/states',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_all_states():
    states_list = []
    states = storage.all(State)
    for key, state in states.items():
        states_list.append(state.to_dict())
    return jsonify(states_list), 200


@app_views.route(
                    '/states/<string:state_id>',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_state(state_id):
    states = storage.all(State)
    new_key = "State" + "." + state_id
    for key, state in states.items():
        if key == new_key:
            return jsonify(state.to_dict()), 200
    return abort(404)


@app_views.route(
                    '/states/<string:state_id>',
                    methods=['DELETE'],
                    strict_slashes=False
                    )
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return {}, 200
    return abort(404)


@app_views.route(
                    '/states',
                    methods=['POST'],
                    strict_slashes=False
                    )
def create_state():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, 'Not a JSON' if not data else 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route(
                    '/states/<string:state_id>',
                    methods=['PUT'],
                    strict_slashes=False
                        )
def update_state(state_id):
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200
    return abort(404)
