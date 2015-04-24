#!/usr/bin/env python

import json

from lib.shell import run_command


def to_bool(value):
    if not value:
        return False

    return value.lower() == 'true'

# See https://github.com/michaelklishin/rabbit-hole/blob/master/queues.go#L10
# for description
QUEUE_ATTRIBUTES = [
    # general properties
    ('vhost', str),
    ('name', str),
    ('node', str),
    ('auto_delete', to_bool),
    ('durable', to_bool),

    # queue info
    ('messages', int),
    ('messages_ready', int),
    ('messages_unacknowledged', int),
    ('consumers', int),
    ('memory', int),
    ('state', str),

    # backing store info
    ('backing_queue_status.len', int),
    ('backing_queue_status.pending_acks', int),
    ('backing_queue_status.ram_msg_count', int),
    ('backing_queue_status.ram_ack_count', int),
    ('backing_queue_status.persistent_count', int),
    ('backing_queue_status.avg_ingress_rate', float),
    ('backing_queue_status.avg_egress_rate', float),
    ('backing_queue_status.avg_ack_ingress_rate', float),
    ('backing_queue_status.avg_ack_egress_rate', float)
]


def list_queues():
    cmd = ['rabbitmqadmin', 'list', 'queues']

    for attr_name, attr_type in QUEUE_ATTRIBUTES:
        cmd.append(attr_name)

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

        item = {}
        for index, (attr_name, attr_cast) in enumerate(QUEUE_ATTRIBUTES):
            value = split[index].strip()
            value = attr_cast(value)
            item[attr_name] = value

        result.append(item)

    return result


if __name__ == '__main__':
    result = list_queues()
    print(json.dumps(result))
