from st2common.util import isotime

from lib.base import BaseCubeSensorsAction

FIELD_CONVERT_FUNCS = {
    'time': lambda value: isotime.parse(value),
    'temp': lambda value: (float(value) / 100)
}


class GetDeviceMeasurements(BaseCubeSensorsAction):
    def run(self, device_uid):
        response = self._perform_request('/devices/%s/current' % (device_uid))
        data = response.json()

        values = data['results'][0]
        field_list = data['field_list']

        result = {}
        for index, field_name in enumerate(field_list):
            value = values[index]

            convert_func = FIELD_CONVERT_FUNCS.get(field_name, None)
            if convert_func:
                value = convert_func(value=value)

            result[field_name] = value

        return result
