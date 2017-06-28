
## Quick Queue
A simple implementation of a job queue with Python.

Quickly run multiple jobs in parallel and keep a maximum number of jobs running simultaneously.

## Usage
```
qqueue start 4 & # run 4 jobs in parallel
qqueue add executable # add executable to the job to run
qqueue add executable # add executable to the job to run
...
qqueue status # see how many jobs have started and finished
qqueue wait # block until all jobs finished, then exit the server
```

## TODO/Issues
* We always use the same port. 
* Track jobs that have failed.
* pip installer
