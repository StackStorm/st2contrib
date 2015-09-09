#!/usr/bin/env python

import sys
import json

from lib.shell import run_command


def list_exchanges(vhost=None):
    cmd = ['rabbitmqadmin', 'list', 'exchanges']

    if vhost:
        cmd += ['-V', vhost]

    exit_code, stdout, stderr = run_command(cmd=cmd, shell=False)

    if exit_code != 0:
        msg = 'Command failed: %s' % (stderr)
        raise Exception(msg)

    result = []
    lines = stdout.split('\n')
    lines = [line for line in lines if line.strip()]

    # Ignore header and footer
    lines = lines[3:-1]

    for line in lines:
        split = line.split('|')
        split = split[1:-1]
        item = {
            'vhost': split[0].strip(),
            'name': split[1].strip(),
            'type': split[2].strip(),
            'auto_delete': split[3].strip(),
            'durable': split[4].strip(),
            'internal': split[5].strip(),
        }
        result.append(item)

    return result


if __name__ == '__main__':
    vhost = sys.argv[1] if len(sys.argv) > 1 else None
    vhost = vhost if vhost else None
    result = list_exchanges(vhost=vhost)
    print(json.dumps(result))
