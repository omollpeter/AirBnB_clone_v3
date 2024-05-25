#!/usr/bin/python3
"""
This script is for defining routes using the blueprint instance
"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"})
