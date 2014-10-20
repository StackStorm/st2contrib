#!/usr/bin/python

import sys
from lib import openstack
from keystoneclient.v3.client import Client

os = openstack.OpenStack('config.json')
sess = os.getSession()

client = Client(session=sess)


print os.run(client,sys.argv)
