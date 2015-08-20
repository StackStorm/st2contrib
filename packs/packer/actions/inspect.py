from lib.actions import BaseAction


class InspectAction(BaseAction):
    def run(self, packerfile, cwd=None):
        if cwd:
            self.set_dir()cwd)

        p = self.packer(packerfile)
        result = p.inspect(self, mrf=True)
        return result.parsed_output
