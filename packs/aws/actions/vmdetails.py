#!/usr/bin/python

import os, sys, json, pprint
from st2libs import ec2,st2utils
from st2client.client import Client

st2_endpoints = {
    'action': 'http://localhost:9101',
    'reactor': 'http://localhost:9102',
    'datastore': 'http://localhost:9103'
}

action_args = st2utils.st2args(args=sys.argv,default='id')

try:
  client = Client(st2_endpoints)
  aws_region = client.keys.get_by_name('aws_region').value
except Exception, e:
  print e
  sys.exit(2)


e = ec2.EC2(aws_region)
#e.setup(True)

instances = e.getInstanceDetails(action_args['id'])

if 'json' in action_args.keys():
  print json.dumps(instances)
  sys.exit(0)

if 'iponly' in action_args.keys():
  for i in instances:
    print instances[i]['ip_address']
    sys.exit(0)

for i in instances:
  print "INSTANCE: %s:" % i
  for k in instances[i]:
    if k == 'state_code':
      next
    else:
      print "\t%s : %s" % (k, instances[i][k])
