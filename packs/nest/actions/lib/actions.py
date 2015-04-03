from st2actions.runners.pythonrunner import Action
import nest
from nest import utils as utils

class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._nest = self._get_client()
        self._utils = utils

    def _get_client(self):
        username = self.config['username']
        password = self.config['password']

        napi = nest.Nest(username, password)
        return napi

    def _get_device(self, structure, device):
        return self._nest.structures[structure].devices[device]

    def _get_structure(self, structure):
        return self._nest.structures[structure]

    def _convert_temperature(self, temperature, scale):
        return {
            'fahrenheit': self._utils.f_to_c(temperature),
            'f': self._utils.f_to_c(temperature),
            'celsius': temperature,
            'c': temperature,
            }.get(scale, temperature)
