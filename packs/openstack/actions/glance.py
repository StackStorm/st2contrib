#!/usr/bin/python

import sys, types, json
from lib import openstack
from glanceclient import Client

os = openstack.OpenStack('config.json')
token = os.getToken()
ep = os.endpoints['glance']

client = Client('1', endpoint=ep, token=token)

action = os.run(client,sys.argv)
print action

#results = {sys.argv[0]: []}
#
#if hasattr(action, '__getitem__'):
#  for result in action:
#   results[sys.argv[0]].append(result)
#else:
#  results[sys.argv[0]] = action.to_dict()
#
#print json.dumps(results)

