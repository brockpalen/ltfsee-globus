"""Project global config file using Flask Config"""

# NOTE: Flask global config object ignores the value if not all CAPS


class Config(object):
    """Base class for configuration, all other inherit from this."""

    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite://:memory:'


class ProductionConfig(Config):
    """Production configuration options."""

    # DATABASE_URI = 'mysql://user@localhost/foo'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration options."""

    DEBUG = True
    LTFSEE_LIB = ["tplib_l", "asb_tplib_l"]
    print("APP IN DEBUG MODE. Should not be seen in production")
    # SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Testing configuration options."""

    TESTING = True
