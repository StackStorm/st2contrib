import yaml

action_meta = {
    "name": "",
    "parameters": {
        "cmd": {
            "type": "string",
            "immutable": False,
            "default": ""
        },
        "action": {
            "type": "string",
            "immutable": True,
            "default": ""
        }
    },
    "runner_type": "run-python",
    "description": "",
    "enabled": True,
    "entry_point": "runner.py"}


def create_manifest(action):
    manifest = action_meta
    manifest['name'] = action
    manifest['parameters']['cmd']['default'] = '{0}.help'.format(action)
    manifest['parameters']['action']['default'] = action

    fh = open('{0}.yaml'.format(action), 'w')
    fh.write('---\n')
    fh.write(yaml.dump(manifest, default_flow_style=False))
    fh.close()
