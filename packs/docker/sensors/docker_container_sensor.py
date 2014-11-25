# Requirements:
# See ../requirements.txt
import docker
import six

from st2reactor.sensor.base import PollingSensor


class DockerSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(DockerSensor, self).__init__(sensor_service=sensor_service,
                                           config=config,
                                           poll_interval=poll_interval)
        self._running_containers = {}
        self._ps_opts = None

        self._trigger_pack = 'docker'

        self._started_trigger_ref = '.'.join([self._trigger_pack, 'container_tracker.started'])
        self._stopped_trigger_ref = '.'.join([self._trigger_pack, 'container_tracker.stopped'])

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

    def cleanup(self):
        if getattr(self._client, 'close') is not None:
            self._client.close()

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _dispatch_trigger(self, trigger, container):
        payload = {}
        payload['container_info'] = container
        self._sensor_service.dispatch(trigger, payload)

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
