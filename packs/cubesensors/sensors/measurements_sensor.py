import time

from rauth import OAuth1Session

from st2common.util import isotime
from st2reactor.sensor.base import PollingSensor

__all__ = [
    'CubeSensorsMeasurementsSensor'
]

BASE_URL = 'https://api.cubesensors.com/v1'
FIELD_CONVERT_FUNCS = {
    'temp': lambda value: (float(value) / 100)
}


class CubeSensorsMeasurementsSensor(PollingSensor):
    DATASTORE_KEY_NAME = 'last_measurements_timestamp'

    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(CubeSensorsMeasurementsSensor, self).__init__(sensor_service=sensor_service,
                                                            config=config,
                                                            poll_interval=poll_interval)
        self._device_uids = self._config['sensor'].get('device_uids', [])

        self._logger = self._sensor_service.get_logger(__name__)
        self._device_info_cache = {}
        self._last_measurement_timestamps = {}  # maps device_uid -> last mes. timestamp

    def setup(self):
        if not self._device_uids:
            raise ValueError('No "device_uids" configured!')

        self._session = self._get_session()

        # todo cache deviice names
        # Populate device info cache
        for device_uid in self._device_uids:
            data = self._get_device_info(device_uid=device_uid)
            self._device_info_cache[device_uid] = data

    def poll(self):
        for device_uid in self._device_uids:
            result = self._get_measurements(device_uid=device_uid)

            if not result:
                continue

            self._handle_result(device_uid=device_uid, result=result)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _handle_result(self, device_uid, result):
        existing_last_measurement_timestamp = self._get_last_measurement_timestamp(
            device_uid=device_uid)
        new_last_measurement_timestamp = isotime.parse(result['time'])
        new_last_measurement_timestamp = int(time.mktime(
            new_last_measurement_timestamp.timetuple()))

        if (existing_last_measurement_timestamp and
                new_last_measurement_timestamp <= existing_last_measurement_timestamp):
            # We have already seen this measurement, skip it
            self._logger.debug(('No new measurements, skipping results we have already seen'
                               'for device %s' % (device_uid)))
            return

        # Dispatch trigger
        self._dispatch_trigger(device_uid=device_uid, result=result)

        # Store last measurement timestamp
        self._set_last_measurement_timestamp(
            device_uid=device_uid, last_measurement_timestamp=new_last_measurement_timestamp)

    def _get_last_measurement_timestamp(self, device_uid):
        """
        Retrieve last measurement timestamp for a particular device.

        :rtype: ``int``
        """
        last_measurement_timestamp = self._last_measurement_timestamps.get(device_uid, None)
        if not last_measurement_timestamp:
            name = self._get_datastore_key_name(device_uid=device_uid)
            value = self._sensor_service.get_value(name=name)
            self._last_measurement_timestamps[device_uid] = int(value) if value else 0

        return self._last_measurement_timestamps[device_uid]

    def _set_last_measurement_timestamp(self, device_uid, last_measurement_timestamp):
        """
        Store a last measurement timestamp for a particular device.
        """
        self._last_measurement_timestamps[device_uid] = last_measurement_timestamp

        name = self._get_datastore_key_name(device_uid=device_uid)
        value = self._sensor_service.get_value(name=name)
        value = str(last_measurement_timestamp)
        self._sensor_service.set_value(name=name, value=value)

        return last_measurement_timestamp

    def _get_datastore_key_name(self, device_uid):
        name = self.DATASTORE_KEY_NAME + '.' + device_uid
        return name

    def _dispatch_trigger(self, device_uid, result):
        trigger = 'cubesensors.measurements'

        device_info = self._device_info_cache.get(device_uid, {})
        device_name = device_info.get('extra', {}).get('name', 'unknown')
        payload = {
            'device_uid': device_uid,
            'device_name': device_name,
            'measurements': result
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _get_device_info(self, device_uid):
        response = self._session.get('%s/devices/%s' % (BASE_URL, device_uid))
        data = response.json()
        return data['device']

    def _get_measurements(self, device_uid):
        """
        Retrieve measurements for a particular device.
        """
        response = self._session.get('%s/devices/%s/current' % (BASE_URL, device_uid))
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

    def _get_session(self):
        session = OAuth1Session(consumer_key=self._config['consumer_key'],
                                consumer_secret=self._config['consumer_secret'],
                                access_token=self._config['access_token'],
                                access_token_secret=self._config['access_token_secret'])
        return session
