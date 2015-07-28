from lib.actions import BaseAction
import os


class BuildAction(BaseAction):
    def run(self, packerfile, cwd=None, exclude=None, only=None, variables=None,
            variables_file=None, parallel=True, debug=False, force=False):

        if cwd:
            os.chdir(cwd)

        p = self._packer(packerfile, exc=exclude, only=only, vars=variables, vars_file=variables_file, exec_path=self._exec_path)

        return p.build(parallel=parallel, debug=debug, force=force)
