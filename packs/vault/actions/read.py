from lib import action

class VaultReadAction(action.VaultBaseAction):
    def run(self, path, key=None):
        import json
        return json.dumps(self.vault.read(path)['data'])
