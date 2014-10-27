#!/usr/bin/python

from lib import sensu
import argparse

parser = argparse.ArgumentParser(description='Sensu Aggregate Actions')

parser.add_argument('--check', nargs='?', dest="check")
parser.add_argument('--issued', nargs='?', default=None)
parser.add_argument('--limit', nargs='?', default=None)
parser.add_argument('--offset', nargs='?', default=None)
parser.add_argument('--age', nargs='?', default=None)
parser.add_argument('--summarize', nargs='?', default=None)
parser.add_argument('--results', nargs='?', default=None)
parser.add_argument('--delete', nargs='?', default=None)

args = parser.parse_args()

aggregates = sensu.Aggregates('config.yaml')

if not args.check:
    print(aggregates.list(limit=args.limit, offset=args.offset))
else:
    if args.issued:
        print(aggregates.check_issued(check=args.check, issued=args.issued,
                                      summarize=args.summarize, results=args.results))
    else:
        if args.delete:
            print(aggregates.delete(check=args.check))
        else:
            print(aggregates.check(check=args.check, age=args.age))
