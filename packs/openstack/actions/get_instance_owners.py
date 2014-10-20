#!/usr/bin/python

import sys, types, json
from lib import openstack
from novaclient.client import Client as novaClient
from keystoneclient.v3.client import Client as keystoneClient

ostack = openstack.OpenStack('config.json')
sess = ostack.getSession()

nclient = novaClient('2', session=sess)
kclient = keystoneClient(session=sess)

sys.argv.pop(0)
user_list = {'users':{}}

for server_id in sys.argv:
  nova_request = ("nova servers get server=%s" % server_id).split()

  output = ostack.run(nclient,nova_request)[nova_request[0]]

  vmdetails = {}
  vmdetails['name'] = output['name']
  vmdetails['id'] = output['id']
  user_id = output['user_id']

  keystone_request = ("keystone users get user=%s" % user_id).split()
  output = ostack.run(kclient,keystone_request)[keystone_request[0]]
  
  if output['name'] not in user_list['users'].keys():
    user_list['users']= {output['name']:{'email':output['email']}}
  user_list['users'][output['name']].setdefault('servers', []).append(vmdetails)

print json.dumps(user_list)
