#!/usr/bin/python

import sys, types, json, time
from lib import openstack
from novaclient.client import Client

sys.argv.pop(0)

time.sleep(90)

for server_id in sys.argv:
  os = openstack.OpenStack('config.json')
  sess = os.getSession()
  client = Client('2', session=sess) 
  request = ("nova servers confirm_resize server=%s " % server_id).split()
  servers = os.run(client,request)
  print servers
