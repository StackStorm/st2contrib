#!/usr/bin/python

import sys
from lib import openstack
from keystoneclient.v3.client import Client

ostack = openstack.OpenStack('config.yaml')
sess = ostack.getSession()

client = Client(session=sess)


print(ostack.run(client, sys.argv))
