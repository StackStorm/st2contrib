#!/usr/bin/env python

import httplib
try:
    import simplejson as json
except ImportError:
    import json
import os
import sys
import traceback
from urlparse import urljoin

try:
    import requests
except ImportError:
    raise ImportError('Missing dependency requests. \
                      Do ``pip install requests``.')

try:
    import yaml
except ImportError:
    raise ImportError('Missing dependency pyyaml. \
                      Do ``pip install pyyaml``.')

# ST2 configuration

ST2_CONFIG_FILE = './config.yaml'

ST2_API_BASE_URL = 'http://localhost/api/v1/'
ST2_AUTH_BASE_URL = 'http://localhost/auth/v1/'
ST2_USERNAME = None
ST2_PASSWORD = None
ST2_API_KEY = None
ST2_AUTH_TOKEN = None
ST2_SSL_VERIFY = False

ST2_AUTH_PATH = 'tokens'
ST2_WEBHOOKS_PATH = 'webhooks/st2'
ST2_TRIGGERS_PATH = 'triggertypes'
ST2_TRIGGERTYPE_PACK = 'nagios'
ST2_TRIGGERTYPE_NAME = 'service-state-change'
ST2_TRIGGERTYPE_REF = '.'.join([ST2_TRIGGERTYPE_PACK, ST2_TRIGGERTYPE_NAME])

STATE_MESSAGE = {
    'OK': 'All is well on the Western front.',
    'WARNING': 'We gots a warning yo!',
    'UNKNOWN': 'It be unknown...',
    'CRITICAL': 'Critical!'
}

REGISTERED_WITH_ST2 = False
UNAUTHED = False
IS_API_KEY_AUTH = False

OK_CODES = [httplib.OK, httplib.CREATED, httplib.ACCEPTED, httplib.CONFLICT]
UNREACHABLE_CODES = [httplib.NOT_FOUND]

TOKEN_AUTH_HEADER = 'X-Auth-Token'
API_KEY_AUTH_HEADER = 'St2-Api-Key'
verbose = True


def _create_trigger_type(verbose=False):
    try:
        url = _get_st2_triggers_url()
        payload = {
            'name': ST2_TRIGGERTYPE_NAME,
            'pack': ST2_TRIGGERTYPE_PACK,
            'description': 'Trigger type for nagios event handler.'
        }

        headers = _get_st2_request_headers()
        headers['Content-Type'] = 'application/json; charset=utf-8'

        if verbose:
            print('POST to URL %s for registering trigger. Body = %s, '
                  'headers = %s.\n' % (url, payload, headers))

        post_resp = requests.post(url, data=json.dumps(payload),
                                  headers=headers,
                                  verify=ST2_SSL_VERIFY)
    except:
        traceback.print_exc(limit=20)
        raise Exception('Unable to connect to st2 endpoint %s.' % url)
    else:
        status = post_resp.status_code
        if status in UNREACHABLE_CODES:
            msg = 'Got response %s. Invalid triggers endpoint %s.' \
                'Check configuration!' % (status, url)
            raise Exception(msg)

        if status not in OK_CODES:
            msg = 'Failed to register trigger type %s.%s with st2. ' \
                'HTTP_CODE: %s' % (ST2_TRIGGERTYPE_PACK, ST2_TRIGGERTYPE_NAME,
                                   status)
            raise Exception(msg)
        else:
            print('Registered trigger type with st2.\n')


def _get_auth_url():
    return urljoin(ST2_AUTH_BASE_URL, ST2_AUTH_PATH)


def _get_auth_token(verbose=False):
    # global ST2_AUTH_TOKEN
    auth_url = _get_auth_url()

    if verbose:
        print('Will POST to URL %s to get auth token.\n' % auth_url)

    try:
        resp = requests.post(auth_url,
                            json.dumps({'ttl': 5 * 60}),
                            auth=(ST2_USERNAME, ST2_PASSWORD),
                            verify=ST2_SSL_VERIFY)
    except:
        traceback.print_exc(limit=20)
        raise Exception('Unable to connect to st2 endpoint %s.\n' % auth_url)
    else:
        if resp.status_code in UNREACHABLE_CODES:
            msg = 'Got response %s. Invalid auth endpoint %s. ' \
                'Check configuration!' % (resp.status_code, auth_url)
            raise Exception(msg)
        if resp.status_code not in OK_CODES:
            msg = 'Cannot get a valid auth token from %s. ' \
                'HTTP_CODE: %s' % (auth_url, resp.status_code)
            raise Exception(msg)
        return resp.json()['token']


def _get_st2_request_headers():
    headers = {}

    if not UNAUTHED:
        if IS_API_KEY_AUTH:
            headers[API_KEY_AUTH_HEADER] = ST2_API_KEY
        else:
            if ST2_AUTH_TOKEN:
                headers[TOKEN_AUTH_HEADER] = ST2_AUTH_TOKEN
            else:
                pass

    return headers


def _register_with_st2(verbose=False):
    global REGISTERED_WITH_ST2
    try:
        if not REGISTERED_WITH_ST2:
            if verbose:
                print('Checking if trigger "%s" registered with st2.'
                      % ST2_TRIGGERTYPE_REF)
            _register_trigger_with_st2(verbose=verbose)
            REGISTERED_WITH_ST2 = True
    except:
        traceback.print_exc(limit=20)
        sys.stderr.write(
            'Failed registering with st2. Won\'t post event.\n')
        sys.exit(2)


def _register_trigger_with_st2(verbose=False):
    url = urljoin(_get_st2_triggers_url(), ST2_TRIGGERTYPE_REF)
    sys.stdout.write('GET: %s\n' % url)

    try:
        headers = _get_st2_request_headers()
        if verbose:
            print('Will GET from URL %s for detecting trigger %s. \n' %
                  (url, ST2_TRIGGERTYPE_REF))
            print('Request headers: %s\n' % headers)
        get_resp = requests.get(url, headers=headers, verify=ST2_SSL_VERIFY)
        # else:
        #    get_resp = requests.get(url)
        if get_resp.status_code != httplib.OK:
            _create_trigger_type(verbose=verbose)
        else:
            body = json.loads(get_resp.text)
            if len(body) == 0:
                _create_trigger_type(verbose=verbose)
    except:
        traceback.print_exc(limit=20)
        raise Exception('Unable to connect to st2 endpoint %s.\n' % url)
    else:
        if verbose:
            print('Successfully registered trigger %s with st2.\n'
                  % ST2_TRIGGERTYPE_REF)


def _get_st2_triggers_url():
    url = urljoin(ST2_API_BASE_URL, ST2_TRIGGERS_PATH)
    return url


def _get_st2_webhooks_url():
    url = urljoin(ST2_API_BASE_URL, ST2_WEBHOOKS_PATH)
    return url


def _post_webhook(url, body, verbose=False):
    headers = _get_st2_request_headers()
    headers['X-ST2-Integration'] = 'nagios.'
    headers['St2-Trace-Tag'] = body['payload']['id']
    headers['Content-Type'] = 'application/json; charset=utf-8'

    try:
        if verbose:
            print('Webhook POST: url: %s, headers: %s, body: %s\n'
                  % (url, headers, body))
        r = requests.post(url, data=json.dumps(body), headers=headers,
                          verify=False)
    except:
        raise Exception('Cannot connect to st2 endpoint %s.' % url)
    else:
        status = r.status_code

        if status in UNREACHABLE_CODES:
            msg = 'Webhook URL %s does not exist. Check StackStorm installation!'
            raise Exception(msg)

        if status not in OK_CODES:
            sys.stderr.write('Failed posting nagio event to st2. HTTP_CODE: '
                             '%d\n' % status)
        else:
            sys.stdout.write('Sent nagio event to st2. HTTP_CODE: '
                             '%d\n' % status)


def _post_event_to_st2(payload, verbose=False):
    body = {}
    body['trigger'] = ST2_TRIGGERTYPE_REF

    try:
        body['payload'] = json.loads(payload)
    except:
        print('Invalid JSON payload %s.' % payload)
        sys.exit(3)

    try:
        _post_webhook(url=_get_st2_webhooks_url(), body=body, verbose=verbose)
        return True
    except:
        traceback.print_exc(limit=20)
        print('Cannot send event to st2.')
        # sys.exit(4)
        return False


def _get_payload(host, service, event_id, state, state_type, attempt):
    payload = {}
    payload['host'] = host
    payload['service'] = service
    payload['event_id'] = event_id
    payload['state'] = state
    payload['state_type'] = state_type
    payload['attempt'] = attempt
    payload['msg'] = STATE_MESSAGE.get(state, 'Undefined state.')
    return payload


def main(args):
    event_id = args[1]
    service = args[2]
    state = args[3]
    state_type = args[4]
    attempt = args[5]
    host = args[6]
    verbose = args[7]

    payload = _get_payload(host, service, event_id, state, state_type, attempt)
    body = {}
    body['trigger'] = ST2_TRIGGERTYPE_REF
    body['payload'] = payload
    _post_event_to_st2(payload, verbose=verbose)


if __name__ == '__main__':
    try:
        if not os.path.exists(ST2_CONFIG_FILE):
            sys.stderr.write('Configuration file not found. Exiting.\n')
            sys.exit(1)

        with open(ST2_CONFIG_FILE) as f:
            config = yaml.safe_load(f)
            ST2_USERNAME = config['st2_username']
            ST2_PASSWORD = config['st2_password']
            ST2_API_BASE_URL = config['st2_api_base_url']
            ST2_AUTH_BASE_URL = config['st2_auth_base_url']
        try:
            if not ST2_AUTH_TOKEN:
                print('No auth token found. Let\'s get one from StackStorm!')
                ST2_AUTH_TOKEN = _get_auth_token(verbose=verbose)
        except:
            traceback.print_exc(limit=20)
            print('Unable to negotiate an auth token. Exiting!')
            sys.exit(1)

        if not REGISTERED_WITH_ST2:
            _register_with_st2(verbose=verbose)
    except:
        sys.stderr.write('Failed registering with st2. Won\'t post event.\n')
    else:
        main(sys.argv)
