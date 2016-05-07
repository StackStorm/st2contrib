import yaml
import requests
import requests_mock

from st2tests.base import BaseActionTestCase

from get_ips import GetIPs

__all__ = [
    'GetIPsTestCase'
]

MOCK_CONFIG_BLANK = yaml.safe_load(open(
    'packs/cloudflare/tests/fixture/blank.yaml').read())
MOCK_CONFIG_NO_SCHEMA = yaml.safe_load(open(
    'packs/cloudflare/tests/fixture/no_schema.yaml').read())
MOCK_CONFIG_FULL = yaml.safe_load(open(
    'packs/cloudflare/tests/fixture/full.yaml').read())

MOCK_DATA_INVALID_JSON = "{'dd': doo}"
MOCK_DATA_SUCCESS = open(
    'packs/cloudflare/tests/fixture/success.json').read()
MOCK_DATA_FAIL = open(
    'packs/cloudflare/tests/fixture/fail.json').read()


class GetIPsTestCase(BaseActionTestCase):
    action_cls = GetIPs

    def test_run_no_config(self):
        self.assertRaises(ValueError, GetIPs, MOCK_CONFIG_BLANK)

    def test_run_is_instance(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        self.assertIsInstance(action, GetIPs)

    def test_run_status_no_schema(self):
        action = self.get_action_instance(MOCK_CONFIG_NO_SCHEMA)

        self.assertRaises(requests.exceptions.MissingSchema,
                          action.run)

    def test_run_status_404(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             status_code=404)

        self.assertRaises(ValueError,
                          action.run)

    def test_run_invalid_json(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             text=MOCK_DATA_INVALID_JSON)

        self.assertRaises(ValueError,
                          action.run)

    def test_run_success_true(self):
        expected = {'ipv4_cidrs': [u'199.27.128.0/21'],
                    'ipv6_cidrs': [u'2400:cb00::/32'],
                    'messages': []}

        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             text=MOCK_DATA_SUCCESS)

        result = action.run()
        self.assertEqual(result, expected)

    def test_run_success_flase(self):
        action = self.get_action_instance(MOCK_CONFIG_FULL)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             text=MOCK_DATA_FAIL)
        self.assertRaises(Exception,
                          action.run)
