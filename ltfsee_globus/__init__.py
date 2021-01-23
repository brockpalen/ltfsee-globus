"""Flask Application entrypoint."""
import logging

from flask import Flask
from flask.logging import default_handler
from flask_caching import Cache

root = logging.getLogger()
root.addHandler(default_handler)

app = Flask(__name__)

# Flask Configuration
app.config.from_object("config")

if app.config["DEBUG"] is True:
    root.setLevel(logging.DEBUG)
else:
    root.setLevel(logging.WARNING)

cache = Cache(app)

from apiv05 import blueprint as apiv05

app.register_blueprint(apiv05)
