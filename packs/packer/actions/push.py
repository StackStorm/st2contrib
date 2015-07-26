from lib.actions import BaseAction
import os


class PushAction(BaseAction):
    def run(self, packerfile, cwd):

        if cwd:
            os.chdir(cwd)

        p = self._packer(packerfile, exec_path=self._exec_path)
        return p.push(create=True, atlas_token=self._atlas_token)
