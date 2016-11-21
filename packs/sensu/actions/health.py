#!/usr/bin/python

from lib import sensu
import argparse

parser = argparse.ArgumentParser(description='Sensu Health Check')

parser.add_argument('--consumers', nargs='?', default=False)
parser.add_argument('--messages', nargs='?', default=False)
args = parser.parse_args()

status = sensu.Status()

print status.health(args.consumers, args.messages)
