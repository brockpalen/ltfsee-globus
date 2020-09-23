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

 * pipenv install --dev
 * pipenv shell  ( like venv activate )
 * export FLASK_APP=ltfsee_globus
 * flask run

