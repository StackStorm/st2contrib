import yaml


class StaticMetagen(object):

    action_meta = {
        "name": "",
        "parameters": {
            "action": {
                "type": "string",
                "immutable": True,
                "default": ""
            },
            "host": {
                "description": "Elasticsearch host.",
                "type": "string",
                "required": True
            },
            "url_prefix": {
                "description": "Elasticsearch http url prefix.",
                "type": "string"
            },
            "port": {
                "description": "Elasticsearch port.",
                "type": "string",
            },
            "use_ssl": {
                "description": "Connect to Elasticsearch through SSL.",
                "type": "boolean",
                "default": False
            },
            "http_auth": {
                "description": "Use Basic Authentication ex: user:pass",
                "type": "string"
            },
            "master_only": {
                "description": "Only operate on elected master node.",
                "type": "boolean",
                "default": False
            },
            "timeout": {
                "description": "Don't wait for action completion more then the "
                               "specified timeout.",
                "default": 600,
                "type": "integer"
            },
            "operation_timeout": {
                "description": "Elasticsearch operation timeout in seconds. "
                               "(It's equal to action timeout).",
                "default": "{{timeout}}",
                "immutable": True,
                "type": "string"
            },
            "log_level": {
                "description": "Log level [critical|error|warning|info|debug].",
                "type": "string",
                "default": "warn"
            },
            "dry_run": {
                "description": "Do not perform any changes.",
                "type": "boolean",
                "default": False
            }
        },
        "runner_type": "run-python",
        "description": "Run a Meta Action through a generic Runner.",
        "enabled": True,
        "entry_point": "curator_runner.py"}

    parameter_meta = {
        "type": "string"
    }

    def __init__(self, action_meta=None):
        self.action_meta = StaticMetagen.action_meta
        if action_meta is not None:
            self.action_meta.update(action_meta)

    def generate_action(self, module_type, action):
        manifest = self.action_meta
        manifest['name'] = "{0}_{1}".format(module_type, action)
        manifest['parameters']['action']['default'] = action

        fh = open('{0}_{1}.yaml'.format(module_type, action), 'w')
        fh.write('---\n')
        fh.write(yaml.dump(manifest, default_flow_style=False))
        fh.close()

    def generate_from_file(self, meta_file):
        if meta_file is None:
            return None
        with open(meta_file) as fh:
            actions = yaml.load(fh.read())
        for manifest in self._merge_actions(actions):
            fh = open('{0}.yaml'.format(manifest['name']), 'w')
            fh.write('---\n')
            fh.write(yaml.dump(manifest, default_flow_style=False))
            fh.close()

    def _merge_actions(self, actions):
        for action in actions:
            name, meta = action.items()[0]
            manifest = self.action_meta.copy()
            manifest['name'] = name
            manifest['parameters']['action']['default'] = name

            for k, v in meta['parameters'].items():
                nv = StaticMetagen.parameter_meta.copy()
                nv.update(v)
                meta['parameters'][k] = nv

            parameters = manifest['parameters'].copy()
            parameters.update(meta['parameters'])
            meta['parameters'] = parameters
            manifest.update(meta)

            if 'alias' in manifest:
                alias_name = manifest.pop('alias')
                alias_manifest = manifest.copy()
                alias_manifest['name'] = alias_name
                yield alias_manifest
            yield manifest

metagen = StaticMetagen()
metagen.generate_from_file('lib/curator_actions.yaml')
# print yaml.dump(metagen.meta_actions)
