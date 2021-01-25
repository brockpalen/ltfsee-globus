[![Build Status](https://travis-ci.com/brockpalen/ltfsee-globus.svg?branch=master)](https://travis-ci.com/brockpalen/ltfsee-globus)
[![codecov](https://codecov.io/gh/brockpalen/ltfsee-globus/branch/master/graph/badge.svg)](https://codecov.io/gh/brockpalen/ltfsee-globus)



LTFSEE (Spectrum Archive) Globus
==========

This project aims to bridge Globus.org GCS5 POSIX gateways to understand how to ask LTFSEE to stage mutliple files at once that may exist on tape.  The largest number of files in a transfer that can be given to LTFSEE best allows it to optimize parallel access to data that may suffer from the long lag time spooling to data located on tape.

It provides two compoents

 1. Flask API that runs on nodes running the LTFSEE software and command
 1. Client called by Globus to pass the files one at a time to LTFSEE that are going to be recalled


#### Install using PIPENV


#### Dev options

 * `pipenv install --dev`
 * `pipenv shell`  ( like venv activate )
 * `pytest`
 * `FLASK_DEBUG=True FLASK_ENV=development FLASK_APP=ltfsee_globus AUTH_KEY=changeme CACHE_DEFAULT_TIMEOUT=3 flask run`


#### Caching file states

You if your average recall time per file is high, and globus is sending requests very often you may wish to cache results of `eeadm file state`.

You can do this by setting `CACHE_DEFAULT_TIMEOUT` confuration option.  This will return the last state of each file for `CACHE_DEFAULT_TIMEOUT` seconds before checking with the archive again.

Setting this value to high may reduce messages in `eeadm` logs, but could delay globus starting the transfer of files that are now on disk cache, and slow new files getting into the queue.

## Clients

Packges comes with a few sample clients that can be called directly by Globus, see `clients` README for details.


## Configuration

Configuration is controlled by environment variables using the [Environs](https://pypi.org/project/environs/) package. Values and default are in `config.py`. The default values can be changed by creating a `.env` file or modifying the environment.

## Deploying in production

Given the nature of this API it is recomended you use host side firewall rules to only allow API calls from the Globus servers and not systems that allow user interaction. 

The built in `flask` server is not suitable for production. Currently testing is done with [Gunicorn](https://docs.gunicorn.org/en/stable/settings.html#)

 1. Get SSL Certs
 1. Add `apiuser` service user
 1. Grant `apiuser` `sudo` access to `eeadm` command
 1. Start Gunicorn
 1. ???
=======


## Auth 

Auth is managed by `AUTH_KEY` and clients provide the key in headers `X-API-KEY`.
