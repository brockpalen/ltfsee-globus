"""Flask Application entrypoint."""
from logging.config import fileConfig

from flask import Flask
from flask_caching import Cache

# setup logging configuration
fileConfig("logging.cfg", disable_existing_loggers=False)

app = Flask(__name__)

# Flask Configuration
app.config.from_object("config")

cache = Cache(app)

from apiv05 import blueprint as apiv05

app.register_blueprint(apiv05)
