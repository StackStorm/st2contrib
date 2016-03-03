from lib import action

class VaultDeleteAction(action.VaultBaseAction):
    def run(self, path):
        return self.vault.delete(path)
