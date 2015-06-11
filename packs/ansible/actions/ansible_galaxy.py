#!/usr/bin/env python

import sys
from lib.ansible_base import AnsibleBaseRunner

__all__ = [
    'AnsibleGalaxyRunner'
]


class AnsibleGalaxyRunner(AnsibleBaseRunner):
    """
    Runs Ansible galaxy commands: install/remove/list.
    See: http://docs.ansible.com/galaxy.html
    """
    BINARY_NAME = 'ansible-galaxy'

if __name__ == '__main__':
    AnsibleGalaxyRunner(sys.argv).execute()
