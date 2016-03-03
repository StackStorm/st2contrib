from lib import action


class VaultReadAction(action.VaultBaseAction):
    def run(self, path):
        return self.vault.read(path)['data']
