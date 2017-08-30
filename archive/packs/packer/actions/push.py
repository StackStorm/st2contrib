from lib.actions import BaseAction


class PushAction(BaseAction):
    def run(self, packerfile, name, message=None, cwd=None, exclude=None,
            only=None, variables=None, variables_file=None):
        if cwd:
            self.set_dir(cwd)

        p = self.packer(packerfile, exc=exclude, only=only, variables=variables,
                        vars_file=variables_file)
        if self.atlas_token:
            return p.push(name, message=message, token=self.atlas_token)
        else:
            raise ValueError("Missing 'atlas_token' in config.yaml for packer")
