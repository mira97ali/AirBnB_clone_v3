#!/usr/bin/python3
"""Contains the users view for the API."""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """Retrieves all Users"""
    objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def single_user(user_id):
    """Retrieves User"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    "/users/<user_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def del_user(user_id):
    """Delete User"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """Create User"""
    if not request.is_json:
        abort(400, "Not a JSON")

    new_user = request.get_json()
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    obj = User(**new_user)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """Update User"""
    if not request.is_json:
        abort(400, "Not a JSON")

    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    req = request.get_json()
    for k, v in req.items():
        if k not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
