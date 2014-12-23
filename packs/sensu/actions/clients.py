#!/usr/bin/python

from lib import sensu
import argparse
import sys

parser = argparse.ArgumentParser(description='Sensu Client Actions')

parser.add_argument('--client', nargs='?', dest="client")
parser.add_argument('--history', nargs='?', default=False)
parser.add_argument('--delete', nargs='?', default=False)
parser.add_argument('--limit', nargs='?', default=False)
parser.add_argument('--offset', nargs='?', default=False)
args = parser.parse_args()

clients = sensu.Clients('config.yaml')

if not args.client:
    print(clients.list(limit=args.limit, offset=args.offset))
    sys.exit(0)

if args.history:
    print(clients.history(args.client))
elif args.delete:
    print(clients.delete(args.client))
else:
    print(clients.get(args.client))
