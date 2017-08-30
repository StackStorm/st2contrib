# pylint: disable=line-too-long

import yaml
from .meta import actions

runner_action_meta = {
    "name": "",
    "parameters": {
        "action": {
            "type": "string",
            "immutable": True,
            "default": ""
        },
        "kwargs": {
            "type": "object",
            "required": False
        }
    },
    "runner_type": "run-python",
    "description": "Run Salt Runner functions through Salt API",
    "enabled": True,
    "entry_point": "runner.py"}

local_action_meta = {
    "name": "",
    "parameters": {
        "action": {
            "type": "string",
            "immutable": True,
            "default": ""
        },
        "args": {
            "type": "array",
            "required": False
        },
        "kwargs": {
            "type": "object",
            "required": False
        }
    },
    "runner_type": "run-python",
    "description": "Run Salt Execution modules through Salt API",
    "enabled": True,
    "entry_point": "local.py"}


def generate_actions():
    def create_file(mt, m, a):
        manifest = local_action_meta
        manifest['name'] = "{0}_{1}.{2}".format(mt, m, a)
        manifest['parameters']['action']['default'] = "{0}.{1}".format(m, a)

        fh = open('{0}_{1}.{2}.yaml'.format(mt, m, a), 'w')
        fh.write('---\n')
        fh.write(yaml.dump(manifest, default_flow_style=False))
        fh.close()
    for key in actions:
        map(lambda l: create_file('local', key, l), actions[key])


def sanitize_payload(keys_to_sanitize, payload):
    '''
    Removes sensitive data from payloads before
    publishing to the logs
    '''
    data = payload.copy()
    map(lambda k: data.update({k: "*" * len(payload[k])}), keys_to_sanitize)
    return data
