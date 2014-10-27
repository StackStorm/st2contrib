#!/usr/bin/python

import sys
from lib import openstack
from glanceclient import Client

ostack = openstack.OpenStack('config.yaml')
token = ostack.getToken()
ep = ostack.endpoints['glance']

client = Client('1', endpoint=ep, token=token)

action = ostack.run(client, sys.argv)
print(action)

# results = {sys.argv[0]: []}
#
# if hasattr(action, '__getitem__'):
#  for result in action:
#   results[sys.argv[0]].append(result)
# else:
#  results[sys.argv[0]] = action.to_dict()
#
# print json.dumps(results)
