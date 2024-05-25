#!/usr/bin/python3
"""
This scripts starts flask api application
It also registers blueprints
"""
from flask import Flask
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
