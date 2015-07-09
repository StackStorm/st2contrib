# pylint: disable=line-too-long

runner_action_meta = {
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

local_action_meta = {
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


actions = {
    'archive': ['gunzip', 'gzip', 'rar', 'tar', 'unrar', 'unzip', 'zip_'],
    'cloud': ['action', 'create', 'destroy', 'network_create', 'profile_',
              'virtual_interface_create', 'volume_attach', 'volume_create',
              'volume_delete', 'volume_detach'],
    'cmdmod': ['run', 'run_chroot', 'script'],
    'cp': ['get_file', 'get_url', 'push', 'push_dir'],
    'cron': ['ls', 'rm_job', 'set_job', 'set_env', 'rm_env'],
    'data': ['cas', 'getval', 'update', 'dump'],
    'event': ['fire', 'fire_master', 'send'],
    'file': ['access', 'chgrp', 'chown', 'directory_exists', 'file_exists',
             'find', 'manage_file', 'mkdir', 'remove', 'replace', 'search',
             'symlink', 'touch', 'truncate'],
    'grains': ['append', 'delval', 'get', 'remove', 'setval'],
    'hosts': ['add_hosts', 'get_alias', 'get_ip', 'rm_host', 'set_host'],
    'htpasswd': ['useradd', 'userdel'],
    'mine': ['delete', 'get', 'send', 'update'],
    'network': ['connect', 'ipaddrs', 'interface_ip', 'ping', 'subnets'],
    'pillar': ['get'],
    'pip': ['install', 'freeze', 'uninstall'],
    'pkg': ['install', 'refresh_db', 'remove'],
    'puppet': ['enable', 'disable', 'fact',
               'noop', 'status', 'run', 'summary'],
    'ret': ['get_fun', 'get_jid', 'get_jids', 'get_minions'],
    'saltutil': ['sync_all', 'sync_modules', 'sync_grains', 'sync_outputters',
                 'sync_renderers', 'sync_returners',
                 'sync_states', 'sync_utils'],
    'schedule': ['add', 'delete', 'enable_job', 'disable_job', 'run_job'],
    'service': ['available', 'start', 'restart', 'status', 'stop'],
    'shadow': ['del_password', 'gen_password', 'set_expire', ''],
    'state': ['highstate', 'single', 'sls'],
    'supervisord': ['add', 'remove', 'restart',
                    'reread', 'start', 'stop', 'custom'],
    'systemd': ['available', 'disable', 'restart', 'enable',
                'stop', 'start', 'systemctl_reload'],
    'test': ['ping', 'cross_test', 'echo'],
    'useradd': ['add', 'delete', 'chshell'],

}
