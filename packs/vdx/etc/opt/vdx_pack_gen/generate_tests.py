"""Test generator for VDX pack
"""
import os
import sys
import inspect
import imp
import xml.etree.ElementTree as ET
import yaml
from jinja2 import Template
ROOT_DIR = './pack/actions/'
ST2_REPO_PATH = "/tmp/st2/"
IGNORE_PARAMS = ['username', 'password', 'ip']
TYPICAL_VALUES = {
    'ip_addr': '10.10.0.1/24',
    'inter_type': 'tengigabitethernet',
    'rbridge_id': '224',
    'inter': '10/0/1',
    'vlan_id': '44',
    'vrf': 'test',
    'remote_as': '18003',
    'delete': False,
    'get': False
}


def get_yaml_files():
    """Parse directory and get all YAML files
    """
    yaml_files = []
    for subdir, _, action_files in os.walk(ROOT_DIR):
        for action_file in action_files:
            if 'yaml' in action_file:
                yaml_files.append("%s%s" % (subdir, action_file))

    return yaml_files


def parse_yaml_files(yaml_files):
    """Parse YAML files and add return dictionary of all parsed YAML files
    """
    result = {}
    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as yaml_fd:
            yaml_output = yaml.load(yaml_fd.read())
            result.update({yaml_output['name']: yaml_output})

    return result


def request_user_bool(prompt):
    """Request a yes or no from the user and return the result as a bool
    """
    user_input = raw_input(prompt)
    if user_input is not "y" and user_input is not "n":
        print 'Incorrect entry. Pleasae use "y" or "n".'
        return request_user_bool(prompt)
    else:
        return bool(user_input == "y")


def request_values(actions):
    """Given a dictionary of actions look at its parameters and request
    values for parameters without a default value. This is returned as a
    dictionary adding the `value` filed to the action's dictionary."""
    for action_name, action_metadata in actions.iteritems():
        print "New Action: %s" % action_name
        for parameter, parameter_metadata in\
                action_metadata['parameters'].iteritems():
            if parameter in IGNORE_PARAMS:
                continue

            typical_value = TYPICAL_VALUES.get(parameter, None)
            if typical_value is not None:
                if request_user_bool("  Use typical value (%s) for %s? (y/n):"
                                     % (typical_value, parameter)):
                    actions[action_name]['parameters'][parameter].update(
                        value=typical_value
                    )
                    continue

            default = parameter_metadata.pop('default', None)
            if default is None:
                user_value = raw_input('  Enter value for %s: ' % parameter)
                actions[action_name]['parameters'][parameter].update(
                    value=user_value
                )
            else:
                actions[action_name]['parameters'][parameter].update(
                    value=default
                )

    return actions


class CallbackClass(object):  # pylint:disable=too-few-public-methods
    """Callback class. Contains action_callback method to feed to tests and
    holds results for retriving later.
    """
    result = None

    def action_callback(self, xml, **kwargs):  # pylint:disable=unused-argument
        """Callback for action
        """
        self.result = ET.tostring(xml)


def validate_actions_result(actions, callback):
    """Run each action and confirm with user that the expected result was
    returned.
    """
    invalid_actions = []
    for action, action_metadata in actions.iteritems():
        action_module = imp.load_source(
            action,
            '%s%s' % (ROOT_DIR, action_metadata['entry_point'])
        )
        classes = inspect.getmembers(action_module, predicate=inspect.isclass)
        action_instance = classes[1][1]()
        kwargs = {}
        for parameter, parameter_metadata in\
                action_metadata['parameters'].iteritems():
            if parameter in IGNORE_PARAMS:
                kwargs[parameter] = ' '
            else:
                kwargs[parameter] = parameter_metadata['value']
        kwargs['test'] = True
        kwargs['callback'] = callback.action_callback
        action_instance.run(**kwargs)
        print callback.result
        action_metadata['expected_result'] = callback.result
        actions.update({action: action_metadata})
        if request_user_bool("Does the above output match what you expect?"
                             "(y/n): "):
            action_metadata['expected_result'] = callback.result
            actions.update({action: action_metadata})
        else:
            invalid_actions.append(action)

    return actions, invalid_actions


def generate_test_files(actions, invalid_actions):
    """Generate final tests and write them to disk.
    """
    with open('test_action_template.j2', 'r') as template_file:
        template = Template(template_file.read())
    for action, action_metadata in actions.iteritems():
        if action in invalid_actions:
            print "Skipping %s since its result was deemed invalid." % action
            continue

        expected_result = [
            action_metadata['expected_result'][i:i + 65]
            for i in range(0, len(action_metadata['expected_result']), 65)
        ]

        class_name = 'Test'

        for word in action.split('_'):
            class_name += word.capitalize()

        test_code = template.render(
            action_name=action,
            class_name=class_name,
            parameters=action_metadata['parameters'],
            expected_results=expected_result
        )
        with open("./pack/tests/test_action_%s" %
                  action_metadata['entry_point'], "w+") as test_fd:
            test_fd.write(test_code)


def print_invalid_actions(invalid_actions):
    """Print list of given invalid actions.
    """
    if len(invalid_actions) > 0:
        print "List of actions with incorrect result:"
        for action in invalid_actions:
            print action
    else:
        print "No invalid actions."


def setup():
    """Setup test build environment.
    """
    st2_artifacts = [
        'st2actions',
        'st2common'
    ]
    for artifact in st2_artifacts:
        sys.path.append(ST2_REPO_PATH + artifact)


def write_answer_file(answers):
    """Write answer file to disk.
    """
    with open("answerfile.yaml", "w+") as answer_file:
        answer_file.write(yaml.dump(answers))


def load_answer_file():
    """Write answer file to disk.
    """
    try:
        with open("answerfile.yaml", "r") as answer_file:
            return yaml.load(answer_file.read())
    except EnvironmentError:
        print "An error occoured trying to load the answer file. Continuing."
        return None


def main():
    """Main entry point
    """
    print "Setting up test build env."
    setup()
    print "Getting YAML files from disk."
    yaml_files = get_yaml_files()
    print "Parsing YAML files to get metadata."
    actions = parse_yaml_files(yaml_files)
    result = None
    if request_user_bool(
            "Would you like to attempt to load an answer file? (y/n): "
    ):
        result = load_answer_file()
    if result is None:
        print "Requesting values for actions without default value."
        actions = request_values(actions)
    else:
        actions = result
    if request_user_bool(
            "Would you like to write these answers to an answer"
            "file? (y/n): "
    ):
        write_answer_file(actions)
    print "Validating actions."
    callback = CallbackClass()
    actions, invalid_actions = validate_actions_result(actions, callback)
    print "Generating test files."
    generate_test_files(actions, invalid_actions)
    print_invalid_actions(invalid_actions)
    print "Test files have been generated."


if __name__ == "__main__":
    main()
