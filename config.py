"""Project global config file using Flask Config."""

# NOTE: Flask global config object ignores the value if not all CAPS


class Config(object):
    """Base class for configuration, all other inherit from this."""

    DEBUG = False
    TESTING = False
    CACHE_TYPE = "filesystem"
    CACHE_DEFAULT_TIMEOUT = 3  # seconds to cache
    CACHE_DIR = "/tmp/ltfsee_globus"
    CACHE_OPTIONS = {"mode": 0o400}  # 3 digit linux-style permissions octal mode
    # DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    """Production configuration options."""

    # DATABASE_URI = 'mysql://user@localhost/foo'
    DEBUG = False
    TESTING = False
    LTFSEE_LIB = ["tplib_l", "asb_tplib_l"]


class DevelopmentConfig(Config):
    """Development configuration options."""

    DEBUG = True
    LTFSEE_LIB = ["lib1"]
    print("APP IN DEBUG MODE. Should not be seen in production")
    # SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration options."""

    TESTING = True
