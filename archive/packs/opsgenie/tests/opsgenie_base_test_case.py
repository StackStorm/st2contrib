# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

import yaml
import json

import requests_mock

from st2tests.base import BaseActionTestCase


class OpsGenieBaseActionTestCase(BaseActionTestCase):
    __test__ = False

    def setUp(self):
        super(OpsGenieBaseActionTestCase, self).setUp()

        self._blank_config = self.load_yaml('configs/blank.yaml')
        self._full_config = self.load_yaml('configs/full.yaml')

    def load_yaml(self, filename):
        return yaml.safe_load(self.get_fixture_content(filename))

    def load_json(self, filename):
        return json.loads(self.get_fixture_content(filename))

    @property
    def blank_config(self):
        return self._blank_config

    @property
    def full_config(self):
        return self._full_config

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          self.action_cls,
                          self.blank_config)

    def test_run_is_instance(self):
        action = self.get_action_instance(self.full_config)
        self.assertIsInstance(action, self.action_cls)
        self.assertEqual(action.api_key, "ApiKey")
        self.assertEqual(action.API_HOST, "https://api.opsgenie.com/")

    def _get_mocked_action(self):
        action = self.get_action_instance(self.full_config)
        action.API_HOST = "mock://api.opsgenie.com/"

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        return action, adapter

    def _get_action_invalid_json(self, method, url):
        action, adapter = self._get_mocked_action()
        action.API_HOST = "mock://api.opsgenie.com/"

        adapter.register_uri(method,
                             url,
                             text="{'ffo': bar}")
        return action, adapter

    def _get_action_status_code(self, method, url, status_code):
        action, adapter = self._get_mocked_action()
        action.API_HOST = "mock://api.opsgenie.com/"

        adapter.register_uri(method,
                             url,
                             status_code=status_code)
        return action, adapter
