from lib.actions import BaseAction
import os


class InspectAction(BaseAction):
    def run(self, packerfile, cwd=None):

        if cwd:
            os.chdir(cwd)

        p = self._packer(packerfile, exec_path=self._exec_path)
        result = p.inspect(mrf=True)
        return result.parsed_output
