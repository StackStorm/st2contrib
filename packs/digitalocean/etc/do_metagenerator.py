#!/usr/bin/env python

import inspect
import yaml
import re
import digitalocean


def get_methods(module):
    functions = {}
    pattern = re.compile('[^_].*')
    for member in dir(module):
        foo = getattr(module, member)
        if inspect.ismethod(foo):
            if pattern.match(member):
                functions[member] = {}
                argspec = inspect.getargspec(foo)
                if argspec.defaults is not None:
                    functions[member] = dict(zip(argspec.args[-len(argspec.defaults):],
                                                 argspec.defaults))
                    for arg in argspec.args:
                        if arg not in functions[member] and arg is not 'self':
                            functions[member][arg] = 'required'
    return functions


def generate_meta(actions, pack):

    for action in actions:
        parameters = {}
        action_meta = {
            "name": "",
            "parameters": {
                "action": {
                    "type": "string",
                    "immutable": True,
                    "default": action
                }
            },
            "runner_type": "run-python",
            "description": "",
            "enabled": True,
            "entry_point": "do.py"
        }

        action_meta["name"] = "%s" % action
        for parameter in actions[action]:
            parameters[parameter] = {"type": "string"}
            if isinstance(actions[action][parameter], bool):
                parameters[parameter]['type'] = "boolean"
            if actions[action][parameter] is not None:
                if actions[action][parameter] == 'required':
                    parameters[parameter]['required'] = True
                else:
                    parameters[parameter]['default'] = actions[action][parameter]
        action_meta['parameters'].update(parameters)
        filename = pack + "/actions/" + action + ".yaml"
        fh = open(filename, 'w')
        fh.write(yaml.dump(action_meta, default_flow_style=False))
        fh.close()

actions = get_methods(digitalocean.Manager)

generate_meta(actions, 'digitalocean')
