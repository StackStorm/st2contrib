#!/usr/bin/python

from lib import sensu
import argparse

parser = argparse.ArgumentParser(description='Sensu Event Actions')

parser.add_argument('--client', nargs='?', dest="client")
parser.add_argument('--check', nargs='?', default=False)
parser.add_argument('--delete', nargs='?', default=False)
parser.add_argument('--resolve', nargs='?', default=False)
args = parser.parse_args()

events = sensu.Events('config.yaml')

if not args.client:
    print(events.list_all())
else:
    if args.check:
        if args.delete:
            print(events.delete(client=args.client, check=args.check))
        elif args.resolve:
            print(events.resolve(client=args.client, check=args.check))
        else:
            print(events.get(client=args.client, check=args.check))
    else:
        print(events.list_by_client(client=args.client))
