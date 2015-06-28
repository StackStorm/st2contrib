import yaml

action_meta = {
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


def generate_action(module_type, action):
    manifest = action_meta
    manifest['name'] = "{0}_{1}".format(module_type, action)
    manifest['parameters']['action']['default'] = action

    fh = open('{0}_{1}.yaml'.format(module_type, action), 'w')
    fh.write('---\n')
    fh.write(yaml.dump(manifest, default_flow_style=False))
    fh.close()


def sanitize_payload(keys_to_sanitize, payload):
    data = payload.copy()
    map(lambda key: data.update({key: "*"*len(payload[key])}), keys_to_sanitize)
    return data
