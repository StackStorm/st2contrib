#!/usr/bin/python

import os, sys, re
from st2libs import ec2
from st2client.client import Client

st2_endpoints = {
    'action': 'http://localhost:9101',
    'reactor': 'http://localhost:9102',
    'datastore': 'http://localhost:9103'
}

if len(sys.argv) > 1:
  search = sys.argv[1] 
  pattern = sys.argv[2]
else:
  print "No pattern given."
  sys.exit(2)

try:
  client = Client(st2_endpoints)
  aws_region = client.keys.get_by_name('aws_region').value
except Exception, e:
  print e
  sys.exit(2)


e = ec2.EC2(aws_region)

images = e.getAMI(owner="self")

ami_ids = []

for i in images:
  if search == 'id':
    if re.search(pattern,i):
      print "IMAGE: %s %s" % (i,images[i]['name'])
      ami_ids.append(i)
  elif search == 'name':
    if re.search(pattern,images[i]['name']):
      print "IMAGE: %s %s" % (i,images[i]['name'])
      ami_ids.append(i)
  else:
    print "No images matched criteria: %s %s" % (search,pattern)
    sys.exit(1)

try:
  for q in ami_ids:
    out = e.deregisterAMI(q)
    print out
except Exception, e:
  print e
