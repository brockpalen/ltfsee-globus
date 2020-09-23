"""Flask Application entrypoint."""
import logging

from flask import Flask

from apiv05 import blueprint as apiv05

logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)

# Flask Configuration
app.config.from_object("config.DevelopmentConfig")


app.register_blueprint(apiv05)
