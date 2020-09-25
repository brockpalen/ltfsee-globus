"""Flask Application entrypoint."""
import logging

from flask import Flask
from flask.logging import default_handler

from apiv05 import blueprint as apiv05

root = logging.getLogger()
root.addHandler(default_handler)

app = Flask(__name__)

# Flask Configuration
app.config.from_object("config.DevelopmentConfig")

if app.config["DEBUG"] is True:
    root.setLevel(logging.DEBUG)
else:
    root.setLevel(logging.WARNING)

app.register_blueprint(apiv05)
