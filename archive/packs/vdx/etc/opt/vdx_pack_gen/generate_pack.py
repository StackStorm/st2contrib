"""Generate pack based on inspecting PyNOS package
"""
import inspect
import re
import xml.etree.ElementTree as et
import pkgutil
import yaml
from docutils import core
import pynos.versions.base


def load_modules():
    """Load modules f or parsing
    """
    for _, modname, _ in pkgutil.iter_modules(pynos.versions.base.__path__):
        __import__('pynos.versions.base.' + modname)


def load_methods():
    """Get methods from modules
    """
    classes = []
    for _, module in inspect.getmembers(
            pynos.versions.base,
            predicate=inspect.ismodule
    ):
        classes.append(inspect.getmembers(module, predicate=inspect.isclass))
    methods = {}
    for cls in classes:
        if isinstance(cls, list) and len(cls) > 0:
            cls = cls[0]
        else:
            continue
        methods.update(
            {
                cls[0]: inspect.getmembers(cls[1], predicate=inspect.ismethod)
            }
        )

    return methods


def parse_methods(methods):
    """Parse methods extract docstring and parse dockstring to get parameters
    """
    info = {}
    for name, methods in methods.iteritems():
        method_args = dict()
        for method in methods:
            if method[0][0] == "_":
                continue
            try:
                xml_docstring = et.fromstring(
                    core.publish_doctree(
                        method[1].im_func.func_doc
                    ).asdom().toxml()
                )
                arguments_block = xml_docstring.find('block_quote').\
                    find('definition_list').find('definition_list_item').\
                    find('definition').find('paragraph').text
            except AttributeError, error:
                print error
                continue
            seperated_arguments = arguments_block.split('\n')
            arg = []
            for item in seperated_arguments:
                items = re.findall(r'\s*([A-z0-9_]*)\s*\(([A-z0-9]*)\):'
                                   r'\s*(.*)', item)
                if len(items) > 0:
                    if items[0][0] == "callback":
                        continue
                    arg.append(items[0])
            if xml_docstring.find('paragraph') is not None:
                arg.append(
                    (
                        '__description__',
                        xml_docstring.find('paragraph').text
                    )
                )
            method_args.update({method[0]: arg})
        info.update({name: method_args})
    return info


def generate_pack(info):
    """Generate pack and write to disk.
    """
    for module, methods in info.iteritems():
        for method, args in methods.iteritems():
            action_name = "%s_%s" % (str.lower(module), method)
            action_path = "%s.%s" % (str.lower(module), method)
            code = """from pynos import device
from st2actions.runners.pythonrunner import Action


class %s(Action):
    def run(self, **kwargs):
        conn = (str(kwargs.pop('ip')), str(kwargs.pop('port')))
        auth = (str(kwargs.pop('username')), str(kwargs.pop('password')))
        test = kwargs.pop('test', False)
        callback = kwargs.pop('callback', None)
        with device.Device(
            conn=conn, auth=auth,
            test=test,
            callback=callback
        ) as dev:
            dev.%s(**kwargs)
        return 0\n""" % (action_name, action_path)
            action_yaml = {
                'name': action_name,
                'runner_type': "python-script",
                'description': "",
                'enabled': True,
                'entry_point': "%s.py" % action_name,
                'parameters': {
                    'ip': {
                        'type': 'string',
                        'description': 'IP address of VDX to connect to.',
                        'required': True,
                        'position': 0
                    },
                    'port': {
                        'type': 'string',
                        'description': 'Port to use to connect to VDX.',
                        'required': True,
                        'default': '22',
                        'position': 1
                    },
                    'username': {
                        'type': 'string',
                        'description': 'Username used with authentication.',
                        'required': True,
                        'position': 2
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password used with authentication.',
                        'required': True,
                        'secret': True,
                        'position': 3
                    }
                }
            }
            type_map = {
                'str': 'string',
                'bool': 'boolean',
                'int': 'integer',
                'tuple(str, str)': 'array'
            }
            if len(args) > 0:
                position = 4
                for arg in args:
                    if arg[0] == '__description__':
                        action_yaml['description'] = arg[1]
                        continue
                    if arg[1] == 'function':
                        continue
                    if type_map.get(arg[1]) is None:
                        raise Exception("%s maps to none" % arg[1])
                    yaml_arg = {
                        'type': type_map.get(arg[1]),
                        'description': arg[2],
                        'required': True,
                        'position': position
                    }
                    if arg[1] == 'bool':
                        del yaml_arg['required']
                    position += 1
                    action_yaml['parameters'].update({arg[0]: yaml_arg})

            with open("pack/actions/%s.py" % action_name, "w+") as py_file:
                py_file.write(code)

            with open("pack/actions/%s.yaml" % action_name, "w+") as py_file:
                output = yaml.dump(action_yaml, default_flow_style=False)
                py_file.write(output)


def main():
    """Main entry point
    """
    load_modules()
    methods = load_methods()
    info = parse_methods(methods)
    generate_pack(info)


if __name__ == "__main__":
    main()
