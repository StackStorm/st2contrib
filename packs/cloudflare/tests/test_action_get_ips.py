import yaml
import requests
import requests_mock

from st2tests.base import BaseActionTestCase

from get_ips import GetIPs

__all__ = [
    'GetIPsTestCase'
]

MOCK_CONFIG_BLANK = ""

MOCK_CONFIG_NO_SCHEMA = """
api_host: "api.cloudflare.com"
"""

MOCK_CONFIG_FULL = """
api_host: "mock://api.cloudflare.com"
"""

MOCK_DATA_INVALID_JSON = "{'dd': doo}"

MOCK_DATA_SUCCESS = """
{
  "success": true,
  "errors": [],
  "messages": [],
  "result": {
    "ipv4_cidrs": [
      "199.27.128.0/21"
    ],
    "ipv6_cidrs": [
      "2400:cb00::/32"
    ]
  }
}
"""

MOCK_DATA_FAIL = """
{
  "success": false,
  "errors": ["An Error happened"],
  "messages": [],
  "result": {}
}
"""


class GetIPsTestCase(BaseActionTestCase):
    action_cls = GetIPs

    def test_run_no_config(self):
        config = yaml.safe_load(MOCK_CONFIG_BLANK)

        self.assertRaises(ValueError, GetIPs, config)

    def test_run_status_no_schema(self):
        config = yaml.safe_load(MOCK_CONFIG_NO_SCHEMA)

        action = self.get_action_instance(config)

        self.assertRaises(requests.exceptions.MissingSchema,
                          action.run)

    def test_run_status_404(self):
        config = yaml.safe_load(MOCK_CONFIG_FULL)

        action = self.get_action_instance(config)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             status_code=404)

        self.assertRaises(ValueError,
                          action.run)

    def test_run_invalid_json(self):
        config = yaml.safe_load(MOCK_CONFIG_FULL)

        action = self.get_action_instance(config)

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

        config = yaml.safe_load(MOCK_CONFIG_FULL)

        action = self.get_action_instance(config)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             text=MOCK_DATA_SUCCESS)

        result = action.run()
        self.assertEqual(result, expected)

    def test_run_success_flase(self):
        config = yaml.safe_load(MOCK_CONFIG_FULL)

        action = self.get_action_instance(config)

        adapter = requests_mock.Adapter()
        action.session.mount('mock', adapter)

        adapter.register_uri('GET',
                             "mock://api.cloudflare.com/client/v4/ips",
                             text=MOCK_DATA_FAIL)
        self.assertRaises(Exception,
                          action.run)
