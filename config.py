"""
Project global config file using Flask Config.

All values can be overridden on the CLI or creating a .env file
https://pypi.org/project/environs/

"""

from pathlib import Path
from tempfile import gettempdir

# NOTE: Flask global config object ignores the value if not all CAPS
from environs import Env

env = Env()
env.read_env()

## tape library names if multiple are available list them to load balance across them
## this does assume that all files are available on both libraries

LTFSEE_LIB = env.list("LTFSEE_LIB", default=[])

## sets log level ERROR, INFO, WARNING, DEBUG
## This does not set logging level for core libraries or gunicorn, look in logging.cfg
LOGLEVEL = env.log_level("LOGLEVEL", default="WARNING")

# FLASK Settings
DEBUG = env.bool("FLASK_DEBUG", default=False)
CACHE_TYPE = "filesystem"
CACHE_DEFAULT_TIMEOUT = env.int(
    "CACHE_DEFAULT_TIMEOUT", default=300
)  # seconds to cache
CACHE_DIR = "/tmp/ltfsee_globus"
CACHE_OPTIONS = {"mode": 0o400}  # 3 digit linux-style permissions octal mode
