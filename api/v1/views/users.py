#!/usr/bin/python3
"""users module"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route(
                    '/users',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_all_users():
    users_list = []
    users = storage.all(User)
    for key, user in users.items():
        users_list.append(user.to_dict())
    return jsonify(users_list), 200


@app_views.route(
                    '/users/<string:user_id>',
                    methods=['GET'],
                    strict_slashes=False
                    )
def get_user(user_id):
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return abort(404)


@app_views.route(
                    '/users/<string:user_id>',
                    methods=['DELETE'],
                    strict_slashes=False
                    )
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return {}, 200
    return abort(404)


@app_views.route(
                    '/users',
                    methods=['POST'],
                    strict_slashes=False
                    )
def create_user():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
                    '/users/<string:user_id>',
                    methods=['PUT'],
                    strict_slashes=False
                        )
def update_user(user_id):
    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
    return abort(404)
