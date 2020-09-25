"""Flask Application entrypoint."""
import logging

from flask import Flask

from apiv05 import blueprint as apiv05

app = Flask(__name__)

# Flask Configuration
app.config.from_object("config.DevelopmentConfig")

if app.config["DEBUG"] == True:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

app.register_blueprint(apiv05)
