#!/usr/bin/python

import sys
import json
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

request = (
    "nova hypervisors search hypervisor_match=%s servers=True" %
    compute).split()

hypervisors = ostack.run(client, request)

uuid_list = {'servers': []}

for hv in hypervisors[request[0]]:
    if 'servers' in hv.keys():
        for server in hv['servers']:
            uuid_list['servers'].append(server['uuid'])

if formatting == 'string':
    print(' '.join(uuid_list['servers']))
elif formatting == 'json':
    print(json.dumps(uuid_list))
else:
    print(uuid_list)
