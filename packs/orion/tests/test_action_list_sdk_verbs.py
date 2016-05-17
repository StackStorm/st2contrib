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

from mock import MagicMock

from orion_base_action_test_case import OrionBaseActionTestCase

from list_sdk_verbs import ListSdkVerbs

__all__ = [
    'ListSdkVerbsTestCase'
]


class ListSdkVerbsTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = ListSdkVerbs

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
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

        query_data = self.load_yaml("results_sdk_verbs.yaml")

        action = self.get_action_instance(self.full_config)
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

        query_data = self.load_yaml("results_sdk_verbs.yaml")

        action = self.get_action_instance(self.full_config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(return_value=query_data)

        result = action.run("orion", "PollNow")
        self.assertEqual(result, expected)
