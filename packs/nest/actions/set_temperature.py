from lib import actions


class SetTemperatureAction(actions.BaseAction):
    def run(self, scale, structure=None, device=None, temp=None, temp_low=None, temp_high=None):
        temperature = None
        mode = None

        # Assume temp if a range is not provided
        if temp_low and temp_high:
            temperature = (self._convert_temperature(temp_low, scale),
                           self._convert_temperature(temp_high, scale))
            # Automatically flip the mode to 'range' to accept the range temp
            mode = 'range'
        else:
            temperature = self._convert_temperature(temp, scale)

        if structure and device:
            nest = self._get_device(structure, device)
            if mode:
                nest.mode = mode
            nest.temperature = temperature
        else:
            for structure in self._nest.structures:
                for device in structure.devices:
                    if mode:
                        device.mode = mode
                    device.temperature = temperature

        return temperature
