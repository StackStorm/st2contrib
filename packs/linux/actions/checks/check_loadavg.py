#!/usr/bin/python

import time
import os, sys
time = sys.argv[1]

loadAvgFile = "/proc/loadavg"
cpuInfoFile = "/proc/cpuinfo"
cpus = 0

try:
  fh = open(loadAvgFile,'r')
  load = fh.readline().split()[0:3]
  fh.close()
except:
  print "Error opening %s" % loadAvgFile
  sys.exit(2)

try:
  fh = open(cpuInfoFile,'r')
  for line in fh:
    if "processor" in line:
      cpus += 1
  fh.close()
except:
  print "Error opeing %s" % cpuInfoFile

  
oneMin = "1 min load/core: %s " % str(float(load[0])/cpus)
fiveMin = "5 min load/core: %s " % str(float(load[1])/cpus)
fifteenMin = "15 min load/core: %s " % str(float(load[2])/cpus)

if time == '1' or time == 'one':
  print oneMin
elif time == '5' or time == 'five':
  print fiveMin
elif time == '15' or time == 'fifteen':
  print fifteenMin
else:
  print oneMin + " " + fiveMin + " " + fifteenMin

exit(0)
