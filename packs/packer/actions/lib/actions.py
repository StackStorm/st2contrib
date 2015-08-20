from st2actions.runners.pythonrunner import Action
import packer
import os


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.atlas_token = self.config.get('atlas_token', None)
        self._exec_path = self.config.get('exec_path', None)
        self._global_vars = self.config.get('variables', None)
        self._packer = self._get_client()

    def _get_vars(self, variables):
        if self._global_vars and variables:
            return self._mergedicts(self._global_vars, variables)
        if self._global_vars and not variables:
            return self._global_vars
        else:
            return variables

    # Grabbed from http://stackoverflow.com/a/7205672
    def _mergedicts(dict1, dict2):
        for k in set(dict1.keys()).union(dict2.keys()):
            if k in dict1 and k in dict2:
                if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                    yield (k, dict(mergedicts(dict1[k], dict2[k])))
                else:
                    yield (k, dict2[k])
            elif k in dict1:
                yield (k, dict1[k])
            else:
                yield (k, dict2[k])

    def set_dir(self, directory):
        os.chdir(directory)

    def packer(self, packerfile, exc=None, only=None, vars=None, vars_file=None):
        if os.path.isfile(self._exec_path):
            return packer.Packer
        else:
            raise Exception("Missing packer binary [{}]".format(self._exec_path))

        return packer.Packer(packerfile, exe=exc, only=only, vars=self._get_vars,
                             vars_file=vars_file, exec_path=self._exec_path)
