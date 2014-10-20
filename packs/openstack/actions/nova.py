#!/usr/bin/python

import sys, types, json
from lib import openstack
from novaclient.client import Client

os = openstack.OpenStack('config.json')
sess = os.getSession()

client = Client('2', session=sess)


action = os.run(client,sys.argv)
print action


#results = {sys.argv[0]: []}

#if hasattr(action, '__getitem__'):
#  for result in action:
#   results[sys.argv[0]].append(result.to_dict())
#else:
#  results[sys.argv[0]] = action.to_dict()

#print json.dumps(results)
