#!/usr/bin/python3
"""
This scripts starts flask api application
It also registers blueprints
"""
from flask import Flask, make_response, jsonify
from models import storage
from flask_cors import CORS
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({"error": "Not found"})), 404


@app.errorhandler(400)
def bad_request(error):
    return make_response(error.description), 400


@app.teardown_appcontext
def teardown_db(exception=None):
    """
    Cleans up resources
    """
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
