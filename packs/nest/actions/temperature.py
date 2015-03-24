from lib import actions

class TemperatureAction(actions.BaseAction):
    def run(self, scale, structure, device, temp=None, temp_low=None, temp_high=None):
        if temp:
            temperature = self.convert_temperature(temp, scale)
            print temperature
            for structure in self._nest.structures:
                for device in structure.devices:
                    device.temperature = temperature
        elif temp_low and temp_high:
            temperature = (self.convert_temperature(temp_low, scale),
                           self.convert_temperature(temp_high, scale))
            print temperature
            for structure in self._nest.structures:
                for device in structure.devices:
                    device.mode = 'range'
                    device.temperature = temperature
        else:
            temperature = self._get_device(structure, device).temperature

        return temperature

    def _convert_temperature(self, temp, scale):
        return {
            'fahrenheit': self._utils.f_to_c(temp),
            'f': self._utils.f_to_c(temp),
            'celsius': temp,
            'c': temp,
            }.get(scale, temp)
