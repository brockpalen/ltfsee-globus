"""Flask Application entrypoint."""
from logging.config import fileConfig

from flask import Flask


def create_app(config="config"):
    """Flask applicaiton factory pattern.

    Use the Flask Applicaiton pattern
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    """

    # setup logging configuration
    fileConfig("logging.cfg", disable_existing_loggers=False)

    app = Flask(__name__)

    # Flask Configuration
    app.config.from_object("config")

    from .cache import cache

    cache.init_app(app)

    from apiv05 import blueprint as apiv05

    app.register_blueprint(apiv05)
    return app
