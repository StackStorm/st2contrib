#!/usr/bin/python

import json
import sys

from lib import openstack
from novaclient.client import Client

ostack = openstack.OpenStack('config.yaml')
sess = ostack.getSession()
client = Client('2', session=sess)


compute = sys.argv[1]
if len(sys.argv) > 2:
    formatting = sys.argv[2]
else:
    formatting = 'dict'

request = ("nova hosts update host=%s" % compute).split()
foo = {'maintenance_mode': 'enabled'}
request.append(json.dumps(foo))

updates = ostack.run(client, request)
print(updates)
sys.exit(0)
