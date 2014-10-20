#!/usr/bin/python

import sys, json
from lib import openstack
from cinderclient.client import Client

os = openstack.OpenStack('config.json')
sess = os.getSession()

client = Client('1', session=sess)

action = os.run(client,sys.argv)

for i in action[sys.argv[0]]:
  print i.id
