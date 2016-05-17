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

from list_sdk_verb_args import ListSdkVerbArgs

__all__ = [
    'ListSdkVerbArgsTestCase'
]


class ListSdkVerbArgsTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = ListSdkVerbArgs

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          "orion",
                          "Cirrus.Nodes",
                          "AddNode")

    def test_run_list_verb_arguments(self):
        expected = {'verb_arguments': [
            {'position': 0,
             'name': "node",
             'type': "SolarWinds.NCM.Contracts.InformationService.NCMNode",
             'optional': False}]}

        query_data = []
        query_data.append(self.load_yaml("results_list_sdk_verb_args.yaml"))

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value=True)
        action.query = MagicMock(side_effect=query_data)

        result = action.run("orion", "Cirrus.Nodes", "AddNode")
        self.assertEqual(result, expected)
