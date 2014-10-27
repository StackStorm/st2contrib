#!/usr/bin/python

import sys
from lib import openstack
from cinderclient.client import Client

ostack = openstack.OpenStack('config.yaml')
sess = ostack.getSession()

client = Client('1', session=sess)

action = ostack.run(client, sys.argv)

for i in action[sys.argv[0]]:
    print(i.id)
