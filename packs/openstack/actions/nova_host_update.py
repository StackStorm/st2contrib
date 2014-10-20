#!/usr/bin/python

import sys, types, json
from lib import openstack
from novaclient.client import Client

os = openstack.OpenStack('config.json')
sess = os.getSession()
client = Client('2', session=sess)


compute=sys.argv[1]
if len(sys.argv) > 2:
  formatting = sys.argv[2]
else:
  formatting = 'dict'

request = ("nova hosts update host=%s" % compute).split()
foo = {'maintenance_mode':'enabled'}
request.append(json.dumps(foo))

updates = os.run(client,request)
print updates
sys.exit(0)

if formatting=='string':
  print ' '.join(uuid_list['servers'])
elif formatting=='json':
  print json.dumps(uuid_list)
else:
  print uuid_list
