#!/usr/bin/python

from lib import sensu
import argparse
import sys
import time
import json

parser = argparse.ArgumentParser(description='Sensu Silence Actions')

parser.add_argument('--client', nargs='?', required=True)
parser.add_argument('--check', nargs='?', default=False)
parser.add_argument('--expiration', nargs='?', default=False)
parser.add_argument('--message', default="Stash created by StackStorm")
args = parser.parse_args()

stashes = sensu.Stashes('config.yaml')

data = {}
data['message'] = args.message

current_time = time.time()
data['timestamp'] = int(current_time)

if args.expiration:
    data['expire'] = int(args.expiration)
else:
    expiration = False

path = "silence/%s" % args.client
if args.check:
    path = "%s/%s" % (path, args.check)

data['path'] = path

print(stashes.post_by_path(path, json.dumps(data)))
