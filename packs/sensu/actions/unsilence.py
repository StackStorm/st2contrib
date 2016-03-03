#!/usr/bin/python

from lib import sensu
import argparse

parser = argparse.ArgumentParser(description='Sensu Unsilence Actions')

parser.add_argument('--client', nargs='?', required=True)
parser.add_argument('--check', nargs='?', default=False)
args = parser.parse_args()

stashes = sensu.Stashes('config.yaml')

path = "silence/%s" % args.client
if args.check:
    path = "%s/%s" % (path, args.check)

print(stashes.delete(path))
