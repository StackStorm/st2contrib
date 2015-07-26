from lib.actions import BaseAction
import os


class ValidateAction(BaseAction):
    def run(self, packerfile, cwd):

        if cwd:
            os.chdir(cwd)

        p = self._packer(packerfile, exec_path=self._exec_path)
        return p.validate(syntax_only=False)
