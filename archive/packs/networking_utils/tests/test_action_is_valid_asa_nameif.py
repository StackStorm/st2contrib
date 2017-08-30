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

from networking_utils_base_test_case import NetworkingUtilsBaseActionTestCase

from is_valid_asa_nameif import IsValidNameifAction

__all__ = [
    'IsValidNameifActionTestCase'
]


class IsValidNameifActionTestCase(NetworkingUtilsBaseActionTestCase):
    __test__ = True
    action_cls = IsValidNameifAction

    def test_run_invalid_too_long_nameif(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "a" * 50)

    def test_run_invalid_spaces_nameif(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError,
                          action.run,
                          "foo bar")

    def test_run_valid_nameif(self):
        action = self.get_action_instance()
        result = action.run("outside")
        self.assertTrue(result)
