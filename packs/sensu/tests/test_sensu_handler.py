import json

import mock
import requests
import responses
import unittest2

# XXX: This file uses a lot of globals and shared state.
# We should definitely refactor this at some
# point since we have tests now.
import st2_handler as sensu_handler


__all__ = [
    'SensuHandlerTestCase'
]


class FakeResponse(object):

    def __init__(self, text, status_code, reason):
        self.text = text
        self.status_code = status_code
        self.reason = reason

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        raise Exception(self.reason)


class SensuHandlerTestCase(unittest2.TestCase):

    def test_st2_headers_token_auth(self):
        sensu_handler.IS_API_KEY_AUTH = False
        self.assertEqual(sensu_handler.IS_API_KEY_AUTH, False,
                         'API auth should be off for this test.')
        sensu_handler.ST2_AUTH_TOKEN = 'dummy-token'
        sensu_handler.ST2_API_KEY = 'dummy-api-key'
        headers = sensu_handler._get_st2_request_headers()
        self.assertTrue('X-Auth-Token' in headers)
        self.assertTrue('St2-Api-Key' not in headers)
        self.assertEqual(headers['X-Auth-Token'], 'dummy-token')

    def test_st2_headers_apikey_auth(self):
        sensu_handler.IS_API_KEY_AUTH = True
        self.assertEqual(sensu_handler.IS_API_KEY_AUTH, True,
                         'API auth should be on for this test.')
        sensu_handler.ST2_AUTH_TOKEN = 'dummy-token'
        sensu_handler.ST2_API_KEY = 'dummy-api-key'
        headers = sensu_handler._get_st2_request_headers()
        self.assertTrue('X-Auth-Token' not in headers)
        self.assertTrue('St2-Api-Key' in headers)
        self.assertEqual(headers['St2-Api-Key'], 'dummy-api-key')

    def test_get_st2_auth_url(self):
        sensu_handler.ST2_AUTH_BASE_URL = 'https://localhost/auth/v1/'
        self.assertEqual(sensu_handler._get_auth_url(),
                         'https://localhost/auth/v1/tokens')

    def test_get_st2_triggers_base_url(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        self.assertEqual(sensu_handler._get_st2_triggers_base_url(),
                        'https://localhost/api/v1/triggertypes')

    def test_get_st2_triggers_url(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        self.assertEqual(sensu_handler._get_st2_triggers_url(),
                        'https://localhost/api/v1/triggertypes/sensu.event_handler')

    def test_get_st2_webhooks_url(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        self.assertEqual(sensu_handler._get_st2_webhooks_url(),
                        'https://localhost/api/v1/webhooks/st2')

    @responses.activate
    def test_post_event_to_st2_bad_payload(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.POST, 'https://localhost/api/v1/webhooks/st2',
            json={}, status=202
        )
        payload = {'foo': 'bar'}
        with self.assertRaises(SystemExit) as cm:
            sensu_handler._post_event_to_st2(payload)
        self.assertTrue(cm.exception.code > 0)

    @responses.activate
    def test_get_auth_token(self):
        sensu_handler.ST2_AUTH_BASE_URL = 'https://localhost/auth/v1/'
        responses.add(
            responses.POST, 'https://localhost/auth/v1/tokens',
            json={'token': 'your_auth_token'}, status=202
        )
        token = sensu_handler._get_auth_token()
        self.assertEqual(token, 'your_auth_token')

    @mock.patch('st2_handler._create_trigger_type')
    @responses.activate
    def test_get_trigger_type_trigger_exists(self, mock_method):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.GET, 'https://localhost/api/v1/triggertypes/sensu.event_handler',
            json={'type': 'sensu.event_handler'}, status=200
        )
        sensu_handler._register_trigger_with_st2()
        self.assertFalse(mock_method.called)

    @mock.patch('st2_handler._create_trigger_type')
    @responses.activate
    def test_trigger_creation_trigger_not_exists(self, mock_method):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.GET, 'https://localhost/api/v1/triggertypes/sensu.event_handler',
            json={}, status=404
        )
        sensu_handler._register_trigger_with_st2()
        self.assertTrue(mock_method.called)

    @mock.patch.object(requests, 'post', mock.MagicMock(
        return_value=FakeResponse(json.dumps({}), status_code=200, reason='blah')))
    def test_create_trigger_type(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        sensu_handler._create_trigger_type()
        requests.post.assert_called_once_with('https://localhost/api/v1/triggertypes',
            data='{"description": "Trigger type for sensu event handler.", ' +
                 '"name": "event_handler", "pack": "sensu"}',
            headers={'Content-Type': 'application/json; charset=utf-8'}, verify=False)

    @mock.patch.object(requests, 'post', mock.MagicMock(
        return_value=FakeResponse(json.dumps({}), status_code=200, reason='blah')))
    def test_ssl_verify_on(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        sensu_handler.ST2_SSL_VERIFY = True
        sensu_handler._create_trigger_type()
        requests.post.assert_called_with('https://localhost/api/v1/triggertypes',
            data='{"description": "Trigger type for sensu event handler.", ' +
                 '"name": "event_handler", "pack": "sensu"}',
            headers={'Content-Type': 'application/json; charset=utf-8'}, verify=True
        )

    @responses.activate
    def test_post_event_to_st2_good_payload(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.POST, 'https://localhost/api/v1/webhooks/st2',
            json={}, status=202
        )
        responses.add(
            responses.GET, 'http://localhost:4567/stashes/silence/ma_client',
            json={}, status=404
        )
        responses.add(
            responses.GET, 'http://localhost:4567/stashes/silence/ma_client/ma_check',
            json={}, status=404
        )
        responses.add(
            responses.GET, 'http://localhost:4567/stashes/silence/all/ma_check',
            json={}, status=404
        )
        trigger_payload = {
            'client': {'name': 'ma_client'},
            'check': {'name': 'ma_check'},
            'id': 'foo-check-id'
        }
        ret = sensu_handler._post_event_to_st2(json.dumps(trigger_payload))
        self.assertEqual(ret, True)

    @responses.activate
    def test_post_event_to_st2_sensu_stashed(self):
        sensu_handler.ST2_API_BASE_URL = 'https://localhost/api/v1/'
        responses.add(
            responses.POST, 'https://localhost/api/v1/webhooks/st2',
            json={}, status=202
        )
        responses.add(
            responses.GET, 'http://localhost:4567/stashes/silence/ma_client',
            json={}, status=200
        )
        responses.add(
            responses.GET, 'http://localhost:4567/stashes/silence/ma_client/ma_check',
            json={}, status=200
        )
        responses.add(
            responses.GET, 'http://localhost:4567/stashes/silence/all/ma_check',
            json={}, status=200
        )
        trigger_payload = {
            'client': {'name': 'ma_client'},
            'check': {'name': 'ma_check'},
            'id': 'foo-check-id'
        }
        with self.assertRaises(SystemExit) as cm:
            sensu_handler._post_event_to_st2(json.dumps(trigger_payload))
        self.assertEqual(cm.exception.code, 0)
