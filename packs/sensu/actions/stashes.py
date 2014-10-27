#!/usr/bin/python

from lib import sensu
import argparse
import sys

parser = argparse.ArgumentParser(description='Sensu Stash Actions')

parser.add_argument('--stash', nargs='?', dest="stash")
parser.add_argument('--limit', nargs='?', default=False)
parser.add_argument('--offset', nargs='?', default=False)
parser.add_argument('--path', nargs='?', default=False)
parser.add_argument('--data', nargs='?', default=False)
args = parser.parse_args()

stashes = sensu.Stashes('config.yaml')

if not args.stash:
    print(stashes.list(limit=args.limit, offset=args.offset))
    sys.exit(0)
else:
    if args.path:
        print(stashes.post_by_path(args.path, args.data))
    elif args.data:
        print(stashes.post(args.data))
    else:
        print(stashes.get(args.stash))
