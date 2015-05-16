#!/usr/bin/env python

import sys
from lib.ansible_base import AnsibleBaseRunner

__all__ = [
    'AnsibleRunner'
]


class AnsibleRunner(AnsibleBaseRunner):
    """
    Runs ansible ad-hoc command (single module).
    See: http://docs.ansible.com/intro_adhoc.html
    Modules: http://docs.ansible.com/list_of_all_modules.html
    """
    BINARY_NAME = 'ansible'

if __name__ == '__main__':
    AnsibleRunner(sys.argv).execute()
