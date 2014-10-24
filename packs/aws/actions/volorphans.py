#!/usr/bin/python

import sys, json, re, argparse
from lib import ec2

parser = argparse.ArgumentParser(description='List orphaned volumes')
parser.add_argument('id', help='EC2 Volume ID', nargs='?', default=None)
parser.add_argument('action', help='What to do', nargs='?', default=None)
args = parser.parse_args()

status = 'available'
trash = []

e = ec2.EC2('lib/config.json')

volumes = e.getVolumeDetails(args.id)

for v in volumes:
  if re.search(status,volumes[v]['status']):
    print "VOLUME: %s:" % v
    for k in volumes[v]:
      print "\t%s : %s" % (k, volumes[v][k])
    if args.action is not None:
      trash.append(v)

if len(volumes) == 0:
    print "No orphaned volumes."
    sys.exit(0)

for d in trash:
  if action == 'delete' or action == 'remove':
    print e.deleteVolume(d)
  elif action =='test':
    print "Deleted volume: %s" % d
