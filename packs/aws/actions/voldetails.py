#!/usr/bin/python

import sys, argparse, json
from lib import ec2

parser = argparse.ArgumentParser(description='Show volume information')
parser.add_argument('id', help='EC2 Volume ID', nargs='?', default=None)
args = parser.parse_args()

e = ec2.EC2('config.json')

volumes = e.getVolumeDetails(args.id)

for v in volumes:
  print "VOLUME: %s:" % v
  for k in volumes[v]:
    print "\t%s : %s" % (k, volumes[v][k])
