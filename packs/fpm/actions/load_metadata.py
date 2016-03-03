#!/usr/bin/env python
import sys
import json

DIR = sys.argv.pop + sys.argv.pop
metadata = open(DIR)
print json.load(metadata)
