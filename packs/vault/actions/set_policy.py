from lib import action

class VaultReadAction(action.VaultBaseAction):
    def run(self, path, key=None):
        return self.vault.read(path)
