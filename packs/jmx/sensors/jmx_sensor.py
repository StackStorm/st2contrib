import os
import re

from st2common.util.shell import run_command
from st2reactor.sensor.base import PollingSensor

__all__ = [
    'JMXSensor'
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JMXQUERY_PATH = os.path.join(CURRENT_DIR, '../extern/jmxquery/jmxquery.jar')
JMXQUERY_PATH = os.path.abspath(JMXQUERY_PATH)


class JMXSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(JMXSensor, self).__init__(sensor_service=sensor_service,
                                        config=config,
                                        poll_interval=poll_interval)
        self._trigger_ref = 'jmx.metric'
        self._logger = self._sensor_service.get_logger(__name__)
        self._args = None

    def setup(self):
        self._check_for_java_binary()

        config = self._config
        url = ('service:jmx:rmi:///jndi/rmi://' + config['hostname'] + ':' +
               str(config['port']) + '/jmxrmi')

        args = [
            'java',
            '-classpath',
            JMXQUERY_PATH,
            'jmxquery.JMXQuery',
            '-U',
            url,
            '-O',
            config['object_name'],
            '-A',
            config['attribute_name']
        ]

        if config['username']:
            args.extend(['-username', config['username']])

        if config['password']:
            args.extend(['-password', config['password']])

        attribute_keys = config.get('attribute_keys', None)
        if attribute_keys:
            attribute_keys = ','.join(attribute_keys)
            args.extend(['-K', attribute_keys])

        self._args = args

    def poll(self):
        command = ' '.join(self._args)
        self._logger.debug('Running command: "%s"' % (command))

        exit_code, stdout, _ = run_command(cmd=self._args)

        if 'status err' in stdout:
            split = stdout.split(' ', 3)
            error = split[-1]
            self._logger.warn('Failed to retrieve metrics: %s' % (error))
        else:
            metrics = self._parse_output(output=stdout)

            for metric in metrics:
                self._dispatch_trigger_for_metric(metric=metric)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _check_for_java_binary(self):
        try:
            run_command(cmd=['java'])
        except OSError:
            raise Exception('Java run time environment is not available, aborting...')

    def _dispatch_trigger_for_metric(self, metric):
        assert isinstance(metric, dict)

        config = self._config
        trigger = self._trigger_ref
        payload = {
            'jmx_hostname': config['hostname'],
            'jmx_port': config['port'],
            'object_name': self._config['object_name'],
            'attribute_name': self._config['attribute_name'],
            'attribute_keys': self._config.get('attribute_keys', None),
            'metric': {
                'name': metric['name'],
                'type': metric['type'],
                'value': metric['value']
            }
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)

    def _parse_output(self, output):
        """
        Parse metrics from the provided jmx query output.

        :rtype: ``list``
        """
        lines = re.split('\n', output)

        metrics = []
        for line in lines:
            if 'metric' not in line:
                continue

            split = line.split(' ')
            if len(split) != 4:
                continue

            metric = {
                'name': split[1],
                'type': split[2],
                'value': split[3]
            }
            metrics.append(metric)

        return metrics
