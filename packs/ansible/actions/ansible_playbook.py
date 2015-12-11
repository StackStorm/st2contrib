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
        '--become_method': '--become-method',
        '--become_user': '--become-user',
        '--extra_vars': '--extra-vars',
        '--flush_cache': '--flush-cache',
        '--force_handlers': '--force-handlers',
        '--inventory_file': '--inventory-file',
        '--list_hosts': '--list-hosts',
        '--list_tags': '--list-tags',
        '--list_tasks': '--list-tasks',
        '--module_path': '--module-path',
        '--private_key': '--private-key',
        '--skip_tags': '--skip-tags',
        '--start_at_task': '--start-at-task',
        '--syntax_check': '--syntax-check',
        '--vault_password_file': '--vault-password-file',
    }

if __name__ == '__main__':
    AnsiblePlaybookRunner(sys.argv).execute()
