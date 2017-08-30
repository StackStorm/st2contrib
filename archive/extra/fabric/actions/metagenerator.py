#!/usr/bin/python

import sys, re
import fabric.docs
import fabric, simplejson, inspect, pprint
from lib import fabfile

action_dir = "./"

def generate_meta(fabfile):
 for i in dir(fabfile):
  action_meta = {}
  fabtask = getattr(fabfile,i)
  if isinstance(fabtask,fabric.tasks.WrappedCallableTask):
    print "%s is a Fabric Callable Task..." % i
    fabparams = getArgs(i,fabfile)
    print "\n"
    try:
      action_meta['name'] = fabtask.wrapped.func_name
      action_meta['description'] =  fabtask.wrapped.func_doc
    except TypeError, e:
      print e
      next
    action_meta['entry_point'] = "fabaction.py"
    action_meta['runner_type'] = "run-local-script"
    action_meta['enabled'] = True

    parameters = {}
    parameters['kwarg_op'] = {"immutable": True, "type": "string", "default": ""}
    parameters['user'] = {"immutable": True}
    parameters['dir'] = {"immutable": True}
    parameters["task"] = {  "type": "string",
                            "description": "task name to be executed",
                            "immutable": True,
                            "default": fabtask.wrapped.func_name }
    if fabparams:
      parameters.update(fabparams)
    action_meta['parameters'] = parameters

    fname = action_dir + action_meta['name'] + ".json"
    try:
      print "Writing %s..." % fname
      fh = open(fname, 'w')
      fh.write(simplejson.dumps(action_meta,indent=2,sort_keys=True))
    except:
      print "Could not write file %s" % fname
      next

    print "\n"

def getArgs(task, fabfile):
  args = {}
  sourcelines = inspect.getsourcelines(fabfile)[0]
  for i, line in enumerate(sourcelines):
    line = line.rstrip()
    pattern = re.compile('def ' + task + '\(')
    if pattern.search(line):
      filtered = filter(None,re.split('\((.*)\):.*',line))
      if len(filtered) < 2:
        return None

      argstring = filtered[1]
      for arg in argstring.split(','):
        if re.search('=',arg):
          arg,v = arg.split('=')
          if v == "''" or v == '""' or v == 'None':
            value={"type":"string"}
          else:
            value={"type":"string","default":v.strip()}
        else:
          value={"type":"string"}
        args[arg.strip()]=value
  return args

generate_meta(fabfile)
