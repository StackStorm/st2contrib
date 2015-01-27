#!/usr/bin/env python2.7

import sys
import os
import subprocess
import select

# Starts command in subprocess processing output as it appears.
def shell_out(command, env={}):
    env = os.environ.copy().update(env)
    proc = subprocess.Popen(args=command, stdin=None, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=env)
    while True:
        fdlist = [proc.stdout.fileno(), proc.stderr.fileno()]
        ios = select.select(fdlist, [], [])
        for fd in ios[0]:
            if fd == proc.stdout.fileno():
                sys.stdout.write(proc.stdout.read())
            else:
                sys.stderr.write(proc.stderr.read())

        if proc.poll() != None: break
    return proc.returncode
