
## Quick Queue
A simple implementation of a job queue with Python.

Quickly run multiple jobs in parallel and keep a maximum number of jobs running simultaneously.

## Installation
```
pip install git+https://github.com/supernifty/qqueue
```

## Usage
```
qqueue start 4 & # run 4 jobs in parallel
qqueue add executable # add executable to the job to run
qqueue add executable # add executable to the job to run
...
qqueue status # see how many jobs have started and finished
qqueue wait # block until all jobs finished, then exit the server
```
### Example

Calculating the md5sum for a large number of files on an 8 core machine

```
# start the server
qqueue start 8 &
sleep 5

# queue all the jobs
for filename in filename_list; do
  qqueue add "md5sum $f > $f.md5"
done

# wait for all jobs to finish
qqueue wait
```

## Options

* --port: run the queue on a different network port
* --verbose: include debugging info
* --version: show the software version

## TODO/Issues
* threaded requests (handle requests while join is in play)
