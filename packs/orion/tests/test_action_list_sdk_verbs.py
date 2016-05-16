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
from mock import Mock, MagicMock

from st2tests.base import BaseActionTestCase

from list_sdk_verbs import ListSdkVerbs

__all__ = [
    'ListSdkVerbsTestCase'
]


class ListSdkVerbsTestCase(BaseActionTestCase):
    action_cls = ListSdkVerbs

    def test_run_no_config(self):
        self.assertRaises(ValueError,
                          ListSdkVerbs,
                          yaml.safe_load(
                              self.get_fixture_content('blank.yaml')))

    def test_run_is_instance(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        self.assertIsInstance(action, ListSdkVerbs)

    def test_run_connect_fail(self):
        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = Mock(side_effect=ValueError(
            'Orion host details not in the config.yaml'))

        self.assertRaises(ValueError,
                          action.run,
                          "orion")

    def test_run_listsdk_verbs(self):
        expected = {'Entities': []}
        expected['Entities'].append({'Entity': "Orion.Nodes",
                                     'Method': "Unmanage"})
        expected['Entities'].append({'Entity': "Orion.Nodes",
                                     'Method': "Remanage"})
        expected['Entities'].append({'Entity': "Orion.Nodes",
                                     'Method': "PollNow"})

        query_data = yaml.safe_load(self.get_fixture_content(
            "results_sdk_verbs.yaml"))

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=query_data)

        result = action.run("orion")

        self.assertEqual(result, expected)

    def test_run_listsdk_verbs_filtered(self):
        expected = {'Entities': []}
        expected['Entities'].append({'Entity': "Orion.Nodes",
                                     'Method': "Unmanage"})
        expected['Entities'].append({'Entity': "Orion.Nodes",
                                     'Method': "Remanage"})
        expected['Entities'].append({'Entity': "Orion.Nodes",
                                     'Method': "PollNow"})

        query_data = yaml.safe_load(self.get_fixture_content(
            "results_sdk_verbs.yaml"))

        action = self.get_action_instance(yaml.safe_load(
            self.get_fixture_content('full.yaml')))

        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=query_data)

        result = action.run("orion", "PollNow")

        self.assertEqual(result, expected)
