#!/usr/bin/env python
import json
import requests
from requests.auth import HTTPBasicAuth
import ast
# from git@github.com:mward29/python-k8sclient.git

from st2reactor.sensor.base import Sensor


class ThirdPartyResource(Sensor):
    def __init__(self, sensor_service, config=None):
        super(ThirdPartyResource, self).__init__(sensor_service=sensor_service,
                                                 config=config)
#        self._labels = self._config['labels'].get('thirdpartyresource', [])\

    def setup(self):
        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)
        self._logger.debug('Connecting to Kubernetes via api_client')
        extension = self._config['extension_url']
        KUBERNETES_API_URL = self._config['kubernetes_api_url'] + extension
        user = self._config['user']
        password = self._config['password']
        verify = self._config['verify']
        self.client = requests.get(KUBERNETES_API_URL, auth=HTTPBasicAuth(user, password),
                                   verify=verify, stream=True)
        pass

    def run(self):
        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)
        self._logger.debug('Watch Kubernetes for thirdpartyresource information')
        r = self.client
        lines = r.iter_lines()
        # Save the first line for later or just skip it
#        first_line = next(lines)
        for line in lines:
            io = json.dumps(line)
            n = json.loads(io)
            d_list = ast.literal_eval(n)
            self._k8s_object(d_list=d_list)
#            self._resource_version(d_list=d_list)
        pass

    def _k8s_object(self, d_list):
        # Define some variables
        resource_type = d_list['type']
        object_kind = d_list['object']['kind']
        name = d_list['object']['metadata']['name']
        namespace = d_list['object']['metadata']['namespace']
        uid = d_list['object']['metadata']['uid']
        # Now lets see if labels exist, if so build a trigger
        if 'labels' in d_list['object']['metadata']:
            labels_data = d_list['object']['metadata']['labels']
            self._build_a_trigger(resource_type=resource_type, name=name, labels=labels_data,
                                  namespace=namespace, object_kind=object_kind, uid=uid)
        else:
            print("No Labels for the resource below. Tough to proceed without knowing how \
                  to work with this object.")
            print(name, namespace, uid)
        pass

    def _build_a_trigger(self, resource_type, name, labels, namespace, object_kind, uid):
        trigger = 'kubernetes.thirdpartyobject'
        payload = {
            'resource': resource_type,
            'name': name,
            'labels': labels,
            'namespace': namespace,
            'object_kind': object_kind,
            'uid': uid
        }
        self._logger = self._sensor_service.get_logger(name=self.__class__.__name__)
        self._logger.debug('Triggering Dispatch Now')

        # Create dispatch trigger
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
        pass

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _process_message(self, message):

        pass
