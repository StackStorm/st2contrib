#!/usr/bin/python

from lib import sensu
import argparse
import sys

parser = argparse.ArgumentParser(description='Sensu Check Actions')

parser.add_argument('--check', nargs='?', dest="check")
parser.add_argument('--subscribers', nargs='?', default=False)
parser.add_argument('--request', nargs='?', default=False)
args = parser.parse_args()

checks = sensu.Checks('config.yaml')

if not args.check:
    print(checks.list())
    sys.exit(0)
else:
    if args.request:
        print(checks.request(check=args.check, subscribers=args.subscribers))
    else:
        print(checks.get(check=args.check))
