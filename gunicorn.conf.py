"""Production Gunicorn configuration file.

See: https://docs.gunicorn.org/en/stable/configure.html
"""
import multiprocessing

from environs import Env

env = Env()
env.read_env()

bind = env.str("BIND", default="0.0.0.0:5000")


# SSL Settings
keyfile = env.str("KEYFILE")
certfile = env.str("CERTFILE")


# these generally don't change
workers = multiprocessing.cpu_count()
accesslog = "-"
