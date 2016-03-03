from lib import action

class VaultGetPolicyAction(action.VaultBaseAction):
    def run(self, name):
        print name
        import json
        return json.loads(json.dumps(self.vault.read("/sys/policy/" + name)['rules']))
