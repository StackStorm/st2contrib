#!/usr/bin/python

import sys, types, json
from lib import fabfile

sys.argv.pop(0)

task_args = {}

if len(sys.argv) > 0:
  for arg in sys.argv:
    a = arg.split('=')
    if len(a) > 1:
      task_args[a[0]] = a[1]

task_name = task_args['task']
del task_args['task']

task = getattr(fabfile, task_name)
print task(**task_args)
