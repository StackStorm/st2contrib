from lib.actions import BaseAction


class ValidateAction(BaseAction):
    def run(self, packerfile, cwd=None, exclude=None, only=None, variables=None,
            variables_file=None):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(self, packerfile)
        return p.validate(syntax_only=False)
