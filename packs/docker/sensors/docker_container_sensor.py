# Requirements:
# See ../requirements.txt
import time

import docker
import six


class DockerSensor(object):
    def __init__(self, container_service, config=None):
        self._running_containers = {}
        self._container_service = container_service
        self._config = config
        self._ps_opts = None

        self._poll_interval = 5  # seconds
        self._trigger_pack = 'docker'

        started_trigger = self.get_trigger_types()[0]
        stopped_trigger = self.get_trigger_types()[1]

        self._started_trigger_ref = '.'.join([self._trigger_pack, started_trigger['name']])
        self._stopped_trigger_ref = '.'.join([self._trigger_pack, stopped_trigger['name']])

    def setup(self):
        docker_opts = self._config

        # Assign sane defaults.
        if docker_opts['version'] is None:
            docker_opts['version'] = '1.13'
        if docker_opts['url'] is None:
            docker_opts['url'] = 'unix://var/run/docker.sock'

        self._version = docker_opts['version']
        self._url = docker_opts['url']
        self._timeout = 10
        if docker_opts['timeout'] is not None:
            self._timeout = docker_opts['timeout']
        self._ps_opts = docker_opts['ps_options']
        self._client = docker.Client(base_url=self._url,
                                     version=self._version,
                                     timeout=self._timeout)
        self._running_containers = self._get_active_containers()
        self._poll_interval = docker_opts.get('poll_interval', self._poll_interval)

    def poll(self):
        containers = self._get_active_containers()

        # Stopped
        for id, running_container in six.iteritems(self._running_containers):
            if id not in containers:
                self._dispatch_trigger(trigger=self._stopped_trigger_ref,
                                       container=running_container)

        # Started
        for id, container in six.iteritems(containers):
            if id not in self._running_containers:
                self._dispatch_trigger(trigger=self._started_trigger_ref,
                                       container=container)

        self._running_containers = containers

    def start(self):
        """
        Note: This method is only needed for StackStorm v0.5. Newer versions of
        StackStorm, only require sensor to implement "poll" method and the
        actual poll schedueling is handled outside of the sensor class.
        """
        while True:
            self.poll()
            time.sleep(self._poll_interval)

    def stop(self):
        if getattr(self._client, 'close') is not None:
            self._client.close()

    def get_trigger_types(self):
        """
        Note: This method is only needed for StackStorm v0.5. In newer versions,
        trigger_types are defined in the sensor metadata file.
        """
        return [
            {
                'name': 'container_tracker.started',
                'pack': self._trigger_pack,
                'description': 'Trigger which indicates that a container has been started',
                'payload_schema': {
                    'type': 'object',
                    'properties': {
                        'container_info': {
                            'type': 'object'
                        }
                    }
                }
            },
            {
                'name': 'container_tracker.stopped',
                'pack': self._trigger_pack,
                'description': 'Trigger which indicates that a container has been stopped',
                'payload_schema': {
                    'type': 'object',
                    'properties': {
                        'container_info': {
                            'type': 'object'
                        }
                    }
                }
            }
        ]

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger(self, trigger, container):
        payload = {}
        payload['container_info'] = container
        self._container_service.dispatch(trigger, payload)

    def _get_active_containers(self):
        opts = self._ps_opts
        # Note: We pass all=False since we want to manually detect stopped containers
        containers = self._client.containers(quiet=opts['quiet'], all=False,
                                             trunc=opts['trunc'], latest=opts['latest'],
                                             since=opts['since'], before=opts['before'],
                                             limit=opts['limit'])
        return self._to_dict(containers)

    def _to_dict(self, containers):
        container_tuples = [(container['Id'], container) for container in containers]
        return dict(container_tuples)
