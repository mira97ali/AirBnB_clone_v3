#!/usr/bin/python3
"""Contains the amenities view for the API."""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    """Retrieves all Amenities"""
    objs = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["GET"],
    strict_slashes=False
)
def single_amenities(amenity_id):
    """Retrieves Amenity"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def del_amenities(amenity_id):
    """Delete Amenity"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """Create Amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")

    new_amenity = request.get_json()
    if "name" not in new_amenity:
        abort(400, "Missing name")

    obj = Amenity(**new_amenity)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route(
    "/amenities/<amenity_id>",
    methods=["PUT"],
    strict_slashes=False
)
def put_amenity(amenity_id):
    """Update Amenity"""
    if not request.is_json:
        abort(400, "Not a JSON")

    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    req = request.get_json()
    for k, v in req.items():
        if k not in ["id", "created_at", "update_at"]:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
