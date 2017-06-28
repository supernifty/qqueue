
## Quick Queue
A simple implementation of a job queue with Python.

Quickly run multiple jobs in parallel and keep a maximum number of jobs running simultaneously.

## Installation

## Usage
```
qqueue start 4 & # run 4 jobs in parallel
qqueue add executable # add executable to the job to run
qqueue add executable # add executable to the job to run
...
qqueue status # see how many jobs have started and finished
qqueue wait # block until all jobs finished, then exit the server
```

## Options

* --port: run the queue on a different network port
* --verbose: include debugging info
* --version: show the software version

## TODO/Issues
* pip installer
