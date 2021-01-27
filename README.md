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


# Deploying in production

Given the nature of this API it is recomended you use host side firewall rules to only allow API calls from the Globus servers and not systems that allow user interaction. 

The built in `flask` server is not suitable for production. Currently testing is done with [Gunicorn](https://docs.gunicorn.org/en/stable/settings.html#)

 1. Get SSL Certs
 1. Add `apiuser` service user
 1. Grant `apiuser` `sudo` access to `eeadm` command
 1. Start Gunicorn
 1. ???
=======

## Configuration

Configuration is controlled by environment variables using the [Environs](https://pypi.org/project/environs/) package. Values and default are in `config.py`. The default values can be changed by creating a `.env` file or modifying the environment.

```
# Secret for Auth to API CHANGE ME 
# pass in header as X-API-KEY
AUTH_KEY=test

# SSL Settings
KEYFILE=ssl/gl-build.key
CERTFILE=ssl/gl-build.crt
```

## logging

Logging is controlled in two places

The config file `logging.cfg` is the main interest for setting log levels on specific packages / loggers.

For the flask app logging it's self `app.logger`  use the environment variable `LOGLEVEL=<ERROR|DEBUG|WARNING>` etc.

## Gunicorn


Gunicorn is the production WSGI server used.  It's configuration is held in `gunicorn.conf.py` but most settings should be set via `.env` much like the flask app so configuration doesn't need to go into source control.

*Startup*
```
pipenv run gunicorn --config gunicorn.conf.py 'ltfsee_globus:create_app()'
```

## SSL

*Requesting Certs*

1. `cd ssl`
1. Create Cert signing request with below settings
 1. `openssl req -new -newkey rsa:2048 -nodes -subj '/emailAddress=arcts-support@umich.edu/C=US/ST=Michigan/L=Ann Arbor/O=University of Michigan/OU=ARC-TS/CN=servername.arc-ts.umich.edu' -out servername.csr -keyout servername.key`
1. Submit to [WASUP](https://webservices.itcs.umich.edu/)
1. Set needed variables in `.env` for `gunicorn.conf.py`

```
C=US
ST=Michigan
L=Ann Arbor
O=University of Michigan
OU=ARC-TS
CN=${website}
emailAddress=arcts-support@umich.edu
```

## systemd


### Systemd 

Update the systemfile for the user and it's `$HOME` for the locaiton of it's `pipenv`.  That is the only python module that's needed in default space the rest will be pulled into the virtualenv created.

```Unit File
[Unit]
Description=Gunicorn arc-slurm-api shim
After=network.target

[Service]
User=brockp
Group=brockp
WorkingDirectory=/home/brockp/arc-slurm-api
ExecStart=/home/brockp/.local/bin/pipenv run gunicorn --config gunicorn.conf.py 'arc_slurm_api:create_app()'

[Install]
WantedBy=multi-user.target
```

Install with

```
systemd enable arc-slurm-api.service
systemd start arc-slurm-api.service
```

### Systemd Alternative 

Often the service user won't have a HOME etc to make pipenv work by default,  we use this alternative that pipenv can use existing virtualenvs.

```
#setup_vnev.sh
#run in the install location of the API Shim
# pipenv will then place all the scripts in that path rather than $HOME/.local/
# this will create a venv
BASEDIR=$(dirname "$0")

cd $BASEDIR
source $BASEDIR/venv/bin/activate
pipenv sync

```

```
{{ ansible_managed | comment }}

# from: https://docs.gunicorn.org/en/stable/deploy.html
[Unit]
Description=Gunicorn arc-slurm-api shim
After=network.target

[Service]
Type=notify
User={{ api_user }}
Group={{ api_group }}
WorkingDirectory={{ api_root }}
ExecStart={{ api_root }}/venv/bin/gunicorn --config gunicorn.conf.py 'ltfsee_globus:create_app()'
KillMode=mixed
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```
