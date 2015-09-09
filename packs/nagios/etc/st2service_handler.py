#!/usr/bin/env python

import httplib
try:
    import simplejson as json
except ImportError:
    import json
import os
import sys
from urlparse import urljoin

try:
    import requests
except ImportError:
    raise ImportError('Missing dependency requests. Do ``pip install requests``.')

try:
    import yaml
except ImportError:
    raise ImportError('Missing dependency pyyaml. Do ``pip install pyyaml``.')

# ST2 configuration
ST2_CONFIG_FILE = './config.yaml'

ST2_API_BASE_URL = 'http://localhost:9101/v1'
ST2_AUTH_BASE_URL = 'http://localhost:9100'
ST2_USERNAME = None
ST2_PASSWORD = None
ST2_AUTH_TOKEN = None

ST2_AUTH_PATH = 'tokens'
ST2_WEBHOOKS_PATH = 'webhooks/st2/'
ST2_TRIGGERS_PATH = 'triggertypes/'
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

OK_CODES = [httplib.OK, httplib.CREATED, httplib.ACCEPTED, httplib.CONFLICT]


def _create_trigger_type():
    try:
        url = _get_st2_triggers_url()
        payload = {
            'name': ST2_TRIGGERTYPE_NAME,
            'pack': ST2_TRIGGERTYPE_PACK,
            'description': 'Trigger type for nagios event handler.'
        }
        # sys.stdout.write('POST: %s: Body: %s\n' % (url, payload))
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'

        if ST2_AUTH_TOKEN:
            headers['X-Auth-Token'] = ST2_AUTH_TOKEN

        post_resp = requests.post(url, data=json.dumps(payload), headers=headers)
    except:
        sys.stderr.write('Unable to register trigger type with st2.')
        raise
    else:
        status = post_resp.status_code
        if status not in OK_CODES:
            sys.stderr.write('Failed to register trigger type with st2. HTTP_CODE: %d\n' %
                             status)
            raise
        else:
            sys.stdout.write('Registered trigger type with st2.\n')


def _get_auth_url():
    return urljoin(ST2_AUTH_BASE_URL, ST2_AUTH_PATH)


def _get_auth_token():
    global ST2_AUTH_TOKEN
    auth_url = _get_auth_url()
    try:
        resp = requests.post(auth_url, json.dumps({'ttl': 5 * 60}),
                             auth=(ST2_USERNAME, ST2_PASSWORD))
    except:
        raise Exception('Cannot get auth token from st2. Will try unauthed.')
    else:
        ST2_AUTH_TOKEN = resp.json()['token']


def _register_with_st2():
    global REGISTERED_WITH_ST2
    try:
        url = urljoin(_get_st2_triggers_url(), ST2_TRIGGERTYPE_REF)
        # sys.stdout.write('GET: %s\n' % url)
        if not ST2_AUTH_TOKEN:
            _get_auth_token()

        if ST2_AUTH_TOKEN:
            get_resp = requests.get(url, headers={'X-Auth-Token': ST2_AUTH_TOKEN})
        else:
            get_resp = requests.get(url)

        if get_resp.status_code != httplib.OK:
            _create_trigger_type()
        else:
            body = json.loads(get_resp.text)
            if len(body) == 0:
                _create_trigger_type()
    except:
        raise
    else:
        REGISTERED_WITH_ST2 = True


def _get_st2_triggers_url():
    url = urljoin(ST2_API_BASE_URL, ST2_TRIGGERS_PATH)
    return url


def _get_st2_webhooks_url():
    url = urljoin(ST2_API_BASE_URL, ST2_WEBHOOKS_PATH)
    return url


def _post_event_to_st2(url, body):
    headers = {}
    headers['X-ST2-Integration'] = 'nagios.'
    headers['Content-Type'] = 'application/json; charset=utf-8'
    if ST2_AUTH_TOKEN:
        headers['X-Auth-Token'] = ST2_AUTH_TOKEN
    try:
        # sys.stdout.write('POST: url: %s, body: %s\n' % (url, body))
        r = requests.post(url, data=json.dumps(body), headers=headers)
    except:
        sys.stderr.write('Cannot connect to st2 endpoint.')
    else:
        status = r.status_code
        if status not in OK_CODES:
            sys.stderr.write('Failed posting nagios event to st2. HTTP_CODE: %d\n' % status)
        else:
            sys.stdout.write('Sent nagios event to st2. HTTP_CODE: %d\n' % status)


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

    payload = _get_payload(host, service, event_id, state, state_type, attempt)
    body = {}
    body['trigger'] = ST2_TRIGGERTYPE_REF
    body['payload'] = payload
    _post_event_to_st2(_get_st2_webhooks_url(), body)


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

        if not REGISTERED_WITH_ST2:
            _register_with_st2()
    except:
        sys.stderr.write('Failed registering with st2. Won\'t post event.\n')
    else:
        main(sys.argv)
