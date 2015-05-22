#!/usr/bin/env python

import sys
from lib.ansible_base import AnsibleBaseRunner

__all__ = [
    'AnsiblePlaybookRunner'
]


class AnsiblePlaybookRunner(AnsibleBaseRunner):
    """
    Runs Ansible playbook.
    See: http://docs.ansible.com/playbooks.html
    """
    BINARY_NAME = 'ansible-playbook'
    REPLACEMENT_RULES = {
        '--verbose=v': '-v',
        '--verbose=vv': '-vv',
        '--verbose=vvv': '-vvv',
        '--verbose=vvvv': '-vvvv',
    }

if __name__ == '__main__':
    AnsiblePlaybookRunner(sys.argv).execute()
