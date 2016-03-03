import json
from lib import action


class VaultGetPolicyAction(action.VaultBaseAction):
    def run(self, name):
        return self.vault.read("/sys/policy/" + name)['rules']
