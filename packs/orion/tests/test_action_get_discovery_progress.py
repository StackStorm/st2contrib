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

# from mock import MagicMock

from orion_base_action_test_case import OrionBaseActionTestCase

from get_discovery_progress import GetDiscoveryProgress
from lib.utils import discovery_status_to_text


__all__ = [
    'GetDiscoveryProgressTestCase'
]


class GetDiscoveryProgressTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = GetDiscoveryProgress

    def test_run_discovery_status_to_text(self):
        status = discovery_status_to_text("0")
        self.assertEqual(status, "Unknown")

        status = discovery_status_to_text("1")
        self.assertEqual(status, "InProgress")

        status = discovery_status_to_text("2")
        self.assertEqual(status, "Finished")

        status = discovery_status_to_text("3")
        self.assertEqual(status, "Error")

        status = discovery_status_to_text("4")
        self.assertEqual(status, "NotScheduled")

        status = discovery_status_to_text("5")
        self.assertEqual(status, "Scheduled")

        status = discovery_status_to_text("6")
        self.assertEqual(status, "NotCompleted")

        status = discovery_status_to_text("7")
        self.assertEqual(status, "Canceling")

        status = discovery_status_to_text("8")
        self.assertEqual(status, "ReadyForImport")

    # FIXME This needs more tests....
    # def test_run_response_processed(self):
    #    pass
