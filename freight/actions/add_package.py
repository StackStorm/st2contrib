#!/usr/bin/env python
import os, sys, glob, json
import subprocess, re

exitcode = 2
output = {}
output['result'] = {}
output['error'] = {}

# Pop off script name
sys.argv.pop(0)
# Repo is last entry, get it then pop it
repos=sys.argv[-1]
sys.argv.pop(-1)
#Remaining items are our list
if re.search('\*',sys.argv[0]):
    files = glob.glob(sys.argv[0])
else:
    files = sys.argv

if re.search(',',repos):
    repos = split(',',repos)
    repos = ' '.join(['apt/%s' % item for item in repos])
else:
    repos = "apt/%s" % repos

for f in files:
    ## Check to see if the file exists
    if os.path.isfile(f):
        call = subprocess.Popen(['freight', 'add', f, repos], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = call.communicate()
        output['result'][f] = stdout
        output['error'][f] = stderr
        exitcode = call.returncode
    else:
        output['result'] = "error"
        exitcode = 1

print json.dumps(output)
sys.exit(exitcode)

