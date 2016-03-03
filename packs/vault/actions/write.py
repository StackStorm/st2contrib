from lib import action

class VaultWriteAction(action.VaultBaseAction):
    def run(self, path, values):
	d = dict(u.split("=") for u in values.split(","))
        return self.vault.write(path, **d) 
