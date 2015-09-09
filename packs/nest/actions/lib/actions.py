from st2actions.runners.pythonrunner import Action
import nest
from nest import utils as utils


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._nest = self._get_client()
        self._utils = utils
        self._structure = self.config['structure']
        self._device = self.config['device']

    def _get_client(self):
        username = self.config['username']
        password = self.config['password']

        napi = nest.Nest(username, password)
        return napi

    def _get_structure(self, structure):
        return self._nest.structures[structure]

    def _get_default_structure(self):
        return self._get_structure(self._structure)

    def _get_device(self, structure, device):
        return self._nest.structures[structure].devices[device]

    def _get_default_device(self):
        return self._get_device(self._structure, self._device)

    def _convert_temperature(self, temperature, scale):
        result = {
            'fahrenheit': self._utils.f_to_c(temperature),
            'f': self._utils.f_to_c(temperature),
            'celsius': temperature,
            'c': temperature
        }
        result = result.get(scale, temperature)
        return result
