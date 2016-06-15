import json

import mock
import requests
import responses
import unittest2

import st2service_handler as nagios_handler


__all__ = [
    'NagiosHandlerTestCase'
]


class FakeResponse(object):

    def __init__(self, test, status_code, reason):
        self.text = test
        self.status_code = status_code
        self.reason = reason

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        raise Exception(self.reason)


class NagiosHandlerTestCase(unittest2.TestCase):

    def test_st2_headers_token_auth(self):
        nagios_handler.IS_API_KEY_AUTH = False
        self.assertEqual(nagios_handler.IS_API_KEY_AUTH, False,
                         'API auth should be off for this test.')
        nagios_handler.ST2_AUTH_TOKEN = 'dummy-token'
        nagios_handler.ST2_API_KEY = 'dummy-api-key'
        headers = nagios_handler._get_st2_request_headers()
        self.assertTrue('X-Auth-Token' in headers)
        self.assertTrue('St2-Api-Key' not in headers)
        self.assertEqual(headers['X-Auth-Token'], 'dummy-token')

    def test_st2_headers_apikey_auth(self):
        nagios_handler.IS_API_KEY_AUTH = True
        self.assertEqual(nagios_handler.IS_API_KEY_AUTH, True,
                         'API auth should be on for this test.')
        nagios_handler.ST2_AUTH_TOKEN = 'dummy-token'
        nagios_handler.ST2_API_KEY = 'dummy-api-key'
        headers = nagios_handler._get_st2_request_headers()
        self.assertTrue('X-Auth-Token' not in headers)
        self.assertTrue('St2-Api-Key' in headers)
        self.assertEqual(headers['St2-Api-Key'], 'dummy-api-key')

    def test_get_st2_auth_url(self):
        nagios_handler.ST2_AUTH_BASE_URL = 'https://localhost/auth/v1/'
        self.assertEqual(nagios_handler._get_auth_url(),
                         'https://localhost/auth/v1/tokens')

    def test_get_st2_triggers_base_url(self):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        self.assertEqual(nagios_handler._get_st2_triggers_base_url(),
                         'https://localhost/api/v1/triggertypes')

    def test_get_st2_triggers_url(self):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        self.assertEqual(nagios_handler._get_st2_triggers_url(),
                         'https://localhost/api/v1/triggertypes/nagios.service_state_change')

    def test_get_st2_webhooks_url(self):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        self.assertEqual(nagios_handler._get_st2_webhooks_url(),
                         'https://localhost/api/v1/webhooks/st2')

    def test_from_arg_to_payload(self):
        nagios_args = ['foo', 'bar']
        with self.assertRaises(SystemExit) as cm:
            nagios_handler._from_arg_to_payload(nagios_args)
        self.assertTrue(cm.exception.code > 0)

    @responses.activate
    def test_get_auth_token(self):
        nagios_handler.ST2_AUTH_BASE_URL = 'https://localhost/auth/v1/'
        responses.add(
            responses.POST, 'https://localhost/auth/v1/tokens',
            json={'token': 'your_auth_token'}, status=202
        )
        token = nagios_handler._get_auth_token()
        self.assertEqual(token, 'your_auth_token')

    @mock.patch('st2service_handler._create_trigger_type')
    @responses.activate
    def test_get_trigger_type_trigger_exists(self, mock_method):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.GET, 'https://localhost/api/v1/triggertypes/nagios.service_state_change',
            json={'type': 'nagios.service_state_change'}, status=200
        )
        nagios_handler._register_trigger_with_st2()
        self.assertFalse(mock_method.called)

    @mock.patch('st2service_handler._create_trigger_type')
    @responses.activate
    def test_trigger_creation_trigger_not_exists(self, mock_method):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.GET, 'https://localhost/api/v1/triggertypes/nagios.service_state_change',
            json={}, status=404
        )
        nagios_handler._register_trigger_with_st2()
        self.assertTrue(mock_method.called)

    @mock.patch.object(requests, 'post', mock.MagicMock(
        return_value=FakeResponse(json.dumps({}), status_code=200, reason='blah')))
    def test_create_trigger_type(self):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        nagios_handler._create_trigger_type()
        requests.post.assert_called_once_with('https://localhost/api/v1/triggertypes',
            data='{"description": "Trigger type for nagios event handler.", ' +
                 '"name": "service_state_change", "pack": "nagios"}',
            headers={'Content-Type': 'application/json; charset=utf-8'}, verify=False)

    @mock.patch.object(requests, 'post', mock.MagicMock(
        return_value=FakeResponse(json.dumps({}), status_code=200, reason='blah')))
    def test_ssl_verify_on(self):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        nagios_handler.ST2_SSL_VERIFY = True
        nagios_handler._create_trigger_type()
        requests.post.assert_called_with('https://localhost/api/v1/triggertypes',
            data='{"description": "Trigger type for nagios event handler.", ' +
                 '"name": "service_state_change", "pack": "nagios"}',
            headers={'Content-Type': 'application/json; charset=utf-8'}, verify=True
        )

    def test_post_event_to_st2_bad_api_url(self):
        nagios_handler.ST2_API_BASE_URL = 'https://localhost/api'
        trigger_payload = {'foo': 'bar'}
        with self.assertRaises(SystemExit) as cm:
            nagios_handler._post_event_to_st2(json.dumps(trigger_payload))
        self.assertTrue(cm.exception.code > 0)
