from lib.actions import BaseAction


class FixAction(BaseAction):
    def run(self, packerfile, outputfile, cwd=None):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(packerfile)
        return p.fix(outputfile)
