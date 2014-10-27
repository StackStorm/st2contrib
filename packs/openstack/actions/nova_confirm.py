#!/usr/bin/python

import sys
import time
from lib import openstack
from novaclient.client import Client

sys.argv.pop(0)

time.sleep(90)

for server_id in sys.argv:
    ostack = openstack.OpenStack('config.yaml')
    sess = ostack.getSession()
    client = Client('2', session=sess)
    request = ("nova servers confirm_resize server=%s " % server_id).split()
    servers = ostack.run(client, request)
    print(servers)
