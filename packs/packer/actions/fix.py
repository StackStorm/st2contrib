from lib.actions import BaseAction
import os


class FixAction(BaseAction):
    def run(self, packerfile, outputfile, cwd=None):

        if cwd:
            os.chdir(cwd)

        p = self._packer(packerfile, exec_path=self._exec_path)
        return p.fix(outputfile)
