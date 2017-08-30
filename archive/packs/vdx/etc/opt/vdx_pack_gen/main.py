"""Pack generation for PyNOS
"""
import generate_pack
import generate_tests


def start_generate_pack():
    """Generate pack
    """
    generate_pack.load_modules()
    methods = generate_pack.load_methods()
    info = generate_pack.parse_methods(methods)
    generate_pack.generate_pack(info)


def start_generate_tests():
    """Generate tests
    """
    print "Setting up test build env."
    generate_tests.setup()
    print "Getting YAML files from disk."
    yaml_files = generate_tests.get_yaml_files()
    print "Parsing YAML files to get metadata."
    actions = generate_tests.parse_yaml_files(yaml_files)
    result = None
    if generate_tests.request_user_bool(
            "Would you like to attempt to load an answer file? (y/n): "
    ):
        result = generate_tests.load_answer_file()
    if result is None:
        print "Requesting values for actions without default value."
        actions = generate_tests.request_values(actions)
    else:
        actions = result
    if generate_tests.request_user_bool(
            "Would you like to write these answers to an answer"
            "file? (y/n): "
    ):
        generate_tests.write_answer_file(actions)
    print "Validating actions."
    callback = generate_tests.CallbackClass()
    actions, invalid_actions = generate_tests.validate_actions_result(
        actions,
        callback
    )
    print "Generating test files."
    generate_tests.generate_test_files(actions, invalid_actions)
    generate_tests.print_invalid_actions(invalid_actions)
    print "Test files have been generated."


def main():
    """Main entry point
    """
    start_generate_pack()
    start_generate_tests()


if __name__ == "__main__":
    main()
