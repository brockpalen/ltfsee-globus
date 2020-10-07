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

Configuration Options:

```
GLOBUS_STAGE_PATH :  Required, path to file being requested to recall from archive, provided by Globus
GLOBUS_STAGE_TASKID : Required, Golbus TaskID, provided by Globus
LTFSEE_URL : Required, Default: http://localhost:5000   URI for API server
DEBUG : Optional, if set (True) print extra messages
```


## advanced_client

More complex client with syslog logging, log level, and NFS remapping if using CES/Protocal nodes with GPFS.


```
GLOBUS_STAGE_PATH :  Required, path to file being requested to recall from archive, provided by Globus
GLOBUS_STAGE_TASKID : Required, Golbus TaskID, provided by Globus
LTFSEE_URL : Default: http://localhost:5000   URI for API server
DEBUG : If set (True) print extra messages
TIMEOUT : Default: 10 Timeout in seconds to pass to requests to wait for API Response
AUTOFS : If set to autofs configuration file will use that file to remap NFS mounts to intenal path in GPFS, else uses /proc/mounts
DEPTH : Default: 4 eg /nfs/dataden/<export> How far to step when remapping 
```
