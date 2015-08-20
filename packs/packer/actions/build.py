from lib.actions import BaseAction


class BuildAction(BaseAction):
    def run(self, packerfile, cwd=None, exclude=None, only=None, variables=None,
            variables_file=None, parallel=True, debug=False, force=False):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(packerfile, exc=exclude, only=only, vars=variables,
                        vars_file=variables_file)
        return p.build(self, parallel=parallel, debug=debug, force=force)
