from lib import action

class VaultReadAction(action.VaultBaseAction):
    def run(self):
        return self.vault.list_policies()
