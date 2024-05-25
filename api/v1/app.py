#!/usr/bin/python3
"""
This scripts starts flask api application
It also registers blueprints
"""
from flask import Flask, make_response, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_404(error):
    return make_response(jsonify({"error": "Not Found"}))


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
