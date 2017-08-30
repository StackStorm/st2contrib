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

from mock import Mock, MagicMock

from orion_base_action_test_case import OrionBaseActionTestCase

from start_discovery import StartDiscovery

__all__ = [
    'StartDiscoveryTestCase'
]


class StartDiscoveryTestCase(OrionBaseActionTestCase):
    __test__ = True
    action_cls = StartDiscovery

    def test_run_connect_fail(self):
        action = self.setup_connect_fail()
        self.assertRaises(ValueError,
                          action.run,
                          name="Unit Test Discovery",
                          poller="primary",
                          snmp_communities=["public"],
                          nodes=["router1"],
                          subnets=None,
                          ip_ranges=None,
                          no_icmp_only=True,
                          auto_import=False)

    def test_run_fail_on_no_targets(self):
        action = self.setup_query_blank_results()

        # nodes = 0, subnets = 0, ip_ranges = 0
        self.assertRaises(ValueError,
                          action.run,
                          name="Unit Test Discovery",
                          poller="primary",
                          snmp_communities=["public"],
                          nodes=None,
                          subnets=None,
                          ip_ranges=None,
                          no_icmp_only=True,
                          auto_import=False)

    def test_run_fail_on_mutliple_targets(self):
        action = self.setup_query_blank_results()

        # nodes = 1, subnets = 1, ip_ranges = 1
        nodes = ["192.168.1.1", "192.168.1.10"]
        subnets = ["192.168.1.0/24"]
        ip_ranges = ["192.168.1.1:192.168.1.10"]

        self.assertRaises(ValueError,
                          action.run,
                          name="Unit Test Discovery",
                          poller="primary",
                          snmp_communities=["public"],
                          nodes=nodes,
                          subnets=subnets,
                          ip_ranges=ip_ranges,
                          no_icmp_only=True,
                          auto_import=False)

        # nodes = 1, subnets = 0, ip_ranges = 1
        nodes = ["192.168.1.1", "192.168.1.10"]
        subnets = None
        ip_ranges = ["192.168.1.1:192.168.1.10"]

        self.assertRaises(ValueError,
                          action.run,
                          name="Unit Test Discovery",
                          poller="primary",
                          snmp_communities=["public"],
                          nodes=nodes,
                          subnets=subnets,
                          ip_ranges=ip_ranges,
                          no_icmp_only=True,
                          auto_import=False)

        # nodes = 1, subnets = 1, ip_ranges = 0
        nodes = ["192.168.1.1", "192.168.1.10"]
        subnets = ["192.168.1.0/24"]
        ip_ranges = None

        self.assertRaises(ValueError,
                          action.run,
                          name="Unit Test Discovery",
                          poller="primary",
                          snmp_communities=["public"],
                          nodes=nodes,
                          subnets=subnets,
                          ip_ranges=ip_ranges,
                          no_icmp_only=True,
                          auto_import=False)

        # nodes = 0, subnets = 1, ip_ranges = 1
        nodes = None
        subnets = ["192.168.1.0/24"]
        ip_ranges = ["192.168.1.1:192.168.1.10"]

        self.assertRaises(ValueError,
                          action.run,
                          name="Unit Test Discovery",
                          poller="primary",
                          snmp_communities=["public"],
                          nodes=nodes,
                          subnets=subnets,
                          ip_ranges=ip_ranges,
                          no_icmp_only=True,
                          auto_import=False)

    def test_run_poller_lookup_primary(self):
        expected = 1

        action = self.get_action_instance(config=self.full_config)

        result = action.get_engine_id("primary")
        self.assertEqual(result, expected)

    def test_run_poller_lookup_fail(self):
        action = self.setup_query_blank_results()
        self.assertRaises(ValueError,
                          action.get_engine_id,
                          "foobar")

    def test_run_snmp_communities_fail(self):
        query_data = []
        query_data.append(self.query_no_results)
        query_data.append(self.query_no_results)

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)

        self.assertRaises(ValueError,
                          action.get_snmp_cred_id,
                          "foobar")

        self.assertRaises(ValueError,
                          action.get_snmp_cred_id,
                          "internal")

    def test_run_discovery_create_completes(self):
        expected = 10

        query_data = []
        query_data.append(self.load_yaml('results_orion_snmp_cred.yaml'))
        query_data.append({'results': [{'ID': 1}]})

        invoke_data = []
        invoke_data.append("CorePluginConfiguration")
        invoke_data.append(10)

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = Mock(side_effect=invoke_data)

        result = action.run(name="Unit Test Discovery",
                            poller="primary",
                            snmp_communities=["public"],
                            nodes=["router1"],
                            subnets=None,
                            ip_ranges=None,
                            no_icmp_only=True,
                            auto_import=False)

        self.assertEqual(result, expected)

    def test_run_discovery_create_completes_on_poller(self):
        expected = 10

        query_data = []
        query_data.append(self.load_yaml('results_orion_snmp_cred.yaml'))
        query_data.append(self.load_yaml('results_orion_engines.yaml'))
        query_data.append({'results': [{'ID': 1}]})

        invoke_data = []
        invoke_data.append("CorePluginConfiguration")
        invoke_data.append(10)

        action = self.get_action_instance(config=self.full_config)
        action.connect = MagicMock(return_value="orion")
        action.query = MagicMock(side_effect=query_data)
        action.invoke = Mock(side_effect=invoke_data)

        result = action.run(name="Unit Test Discovery",
                            poller="primary",
                            snmp_communities=["public"],
                            nodes=["router1"],
                            subnets=None,
                            ip_ranges=None,
                            no_icmp_only=True,
                            auto_import=False)

        self.assertEqual(result, expected)
