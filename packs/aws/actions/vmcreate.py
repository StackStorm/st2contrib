#!/usr/bin/python

import os, sys, json
from st2libs import ec2
from st2client.client import Client

st2_endpoints = {
    'action': 'http://localhost:9101',
    'reactor': 'http://localhost:9102',
    'datastore': 'http://localhost:9103'
}

ami = sys.argv[1]
instance_type = sys.argv[2]

try:
  client = Client(st2_endpoints)
  aws_region = client.keys.get_by_name('aws_region').value
except Exception, e:
  print e
  sys.exit(2)


e = ec2.EC2(aws_region)
e.setup(True)

print e.createVM(ami,instance_type)
