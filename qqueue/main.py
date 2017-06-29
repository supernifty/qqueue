#!/usr/bin/env python

import argparse
import logging
import multiprocessing
import os
import queue
import socket
import threading

VERSION='0.1'
HOST='127.0.0.1'
PORT=1905
BUFFER=2048

def worker(state):
  def _worker():
    while True:
      logging.debug("waiting...")
      cmd = state['queue'].get() # blocks until job available
      logging.info("running {}...".format(cmd))
      with state['lock']:
        state['queued'] -= 1
        state['running'] += 1
      retcode = os.system(cmd) # run job
      with state['lock']:
        state['running'] -= 1
        if retcode == 0:
          state['finished'] += 1
        else:
          state['failed'] += 1
      logging.info("running {}: done. exit code was {}".format(cmd, retcode))
      state['queue'].task_done()
  return _worker
  
def start_workers(state):
  logging.info('starting {} threads'.format(state['max']))
  for _ in range(state['max']):
    thread = threading.Thread(target=worker(state))
    thread.daemon = True
    thread.start()

def execute(state, arg):
  logging.info("queueing {}".format(arg))
  state['queue'].put(arg)
  with state['lock']:
    state['queued'] += 1
  return "queued"

def status(state, arg):
  with state['lock']:
    return "{} jobs queued, {} jobs running, {} jobs finished. {} jobs failed.".format(state['queued'], state['running'], state['finished'], state['failed'])

def done(state, arg):
  state['queue'].join()
  state['done'] = True
  with state['lock']:
    return "{} jobs queued, {} jobs running, {} jobs finished. {} jobs failed.".format(state['queued'], state['running'], state['finished'], state['failed'])

def start(args):

  handler = {
    'E': execute, 
    'S': status,
    'W': done
  }

  state = { 'max': args.jobs, 'queued': 0, 'running': 0, 'finished': 0, 'failed': 0, 'queue': queue.Queue(), 'lock': multiprocessing.Lock(), 'done': False }

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((HOST, args.port))
  server.listen(10)
  logging.info("listening on {}:{}".format(HOST, args.port))

  start_workers(state)

  while not state['done']:
    client, address = server.accept()
    logging.debug("client connected")
    msg = ''
    while True:
      data = client.recv(BUFFER)
      if data:
        msg += data.decode()
      else:
        break
      logging.debug(msg)
      if msg[0] in handler:
        response = handler[msg[0]](state, msg[1:])
      else:
        response = 'Unrecognized command'
      client.send(response.encode())
    logging.debug("client disconnected")
  logging.info("done")

def connect(msg, port):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  logging.debug("client connecting...")
  client.connect((HOST, port))
  logging.debug("client sending...")
  client.send(msg.encode())
  response = client.recv(BUFFER).decode()
  logging.debug("response: {}".format(response))
  client.close()
  logging.debug("client closed...")
  return response


def add(args):
  print(connect('E{}'.format(args.executable), args.port))

def client_status(args):
  print(connect('S', args.port))

def client_wait(args):
  print(connect('W', args.port))

def main():
  parser = argparse.ArgumentParser(description='Run jobs in parallel')

  parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)
  parser.add_argument('--verbose', required=False, action='store_true')
  parser.add_argument('--port', required=False, type=int, default=PORT, help='port to run on (default {})'.format(PORT))
  
  subparsers = parser.add_subparsers(help='available sub-commands', dest='subcommand')
  subparsers.required = True

  start_parser = subparsers.add_parser('start')
  start_parser.add_argument('jobs', type=int, help='number of jobs to run')
  start_parser.set_defaults(func=start)

  add_parser = subparsers.add_parser('add')
  add_parser.add_argument('executable', help='add a new executable to the queue')
  add_parser.set_defaults(func=add)

  status_parser = subparsers.add_parser('status')
  status_parser.set_defaults(func=client_status)

  wait_parser = subparsers.add_parser('wait')
  wait_parser.set_defaults(func=client_wait)

  args = parser.parse_args()
  if args.verbose: 
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  args.func(args)

if __name__ == '__main__':
  main()
