#!/usr/bin/python3
"""Contains the index view for the API."""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Status"""
    return jsonify(status="OK")


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stat():
    """Number of each objects by type"""
    return jsonify(
        amenities=storage.count("Amenity"),
        cities=storage.count("City"),
        places=storage.count("Place"),
        reviews=storage.count("Review"),
        states=storage.count("State"),
        users=storage.count("User")
    )
