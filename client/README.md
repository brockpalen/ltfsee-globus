# Clients

These are example clients to be called by Globus to consume the API.
They use two variables, filled in by Globus themselves:

* `GLOBUS_STAGE_PATH` : Path to file to requst status/stage from tape
* `GLOZBUS_STAGE_TASKID` :  Globus Task id

## Configuration

All clients use the following environment variables for configuration

* `DEBUG`
* `LTFSEE_URL` Full protocal and name:port of server: eg: `http://tpsrvr1.domain.com:5000`

## simple_client

Basic client, nothing special, 

## advacned_client

More complex client with syslog logging, log level, and NFS remapping if using CES/Protocal nodes with GPFS.
