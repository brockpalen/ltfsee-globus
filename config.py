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

# application settings

## List of configured tape libraries
LTFSEE_LIB = env.list("LTFSEE_LIB", default=["tplib_l", "asb_tplib_l"])

## sets log level ERROR, INFO, WARNING, DEBUG
LOGLEVEL = env.str("LOGLEVEL", default="WARNING").upper()


# FLASK Settings
DEBUG = env.bool("FLASK_DEBUG", default=False)
# TESTING = False

## Cache options,
## https://flask-caching.readthedocs.io/en/latest/
CACHE_TYPE = env.str("CACHE_TYPE", default="filesystem")
CACHE_DEFAULT_TIMEOUT = env.int(
    "CACHE_DEFAULT_TIMEOUT", default=300
)  # seconds to cache

cache_dir_def = Path(gettempdir()) / "ltfsee_globus"
CACHE_DIR = env.str(
    "CACHE_DIR", default=str(cache_dir_def)
)  # used for CACHE_TYPE filesystem
CACHE_OPTIONS = env.dict(
    "CACHE_OPTIONS", default={"mode": 0o400}
)  # 3 digit linux-style permissions octal mode
