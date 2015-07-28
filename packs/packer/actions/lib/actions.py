from st2actions.runners.pythonrunner import Action
import packer
import os


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._exec_path = self.config.get('exec_path', '/opt/packer/bin/packer')
        self._atlas_token = self.config.get('atlas_token', None)
        self._packer = self._get_client()

    def _get_client(self):
        if os.path.isfile(self._exec):
            return packer.Packer
        else:
            Exception("Missing packer binary at {}".format(self._exec))
