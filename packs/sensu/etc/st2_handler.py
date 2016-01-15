#!/usr/bin/env python

import base64
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
    requests.packages.urllib3.disable_warnings()
except ImportError:
    raise ImportError('Missing dependency "requests". \
        Do ``pip install requests``.')

try:
    import yaml
except ImportError:
    raise ImportError('Missing dependency "pyyaml". \
        Do ``pip install pyyaml``.')

# ST2 configuration

ST2_API_BASE_URL = 'http://localhost:9101/v1'
ST2_AUTH_BASE_URL = 'http://localhost:9100'
ST2_USERNAME = None
ST2_PASSWORD = None
ST2_AUTH_TOKEN = None

ST2_AUTH_PATH = 'auth/tokens'
ST2_WEBHOOKS_PATH = 'api/webhooks/st2/'
ST2_TRIGGERS_PATH = 'api/triggertypes/'
ST2_TRIGGERTYPE_PACK = 'sensu'
ST2_TRIGGERTYPE_NAME = 'event_handler'
ST2_TRIGGERTYPE_REF = '.'.join([ST2_TRIGGERTYPE_PACK, ST2_TRIGGERTYPE_NAME])

REGISTERED_WITH_ST2 = False

OK_CODES = [httplib.OK, httplib.CREATED, httplib.ACCEPTED, httplib.CONFLICT]


def _get_headers():
    b64auth = base64.b64encode(
        "%s:%s" %
        (SENSU_USER, SENSU_PASS))
    auth_header = "BASIC %s" % b64auth
    content_header = "application/json"
    return {"Authorization": auth_header, "Content-Type": content_header}


def _check_stash(client, check):
    sensu_api = "http://%s:%i" % (SENSU_HOST, SENSU_PORT)
    endpoints = [
        "silence/%s" % client,
        "silence/%s/%s" % (client, check),
        "silence/all/%s" % check]

    for endpoint in endpoints:
        url = "%s/stashes/%s" % (sensu_api, endpoint)
        response = requests.get(url, headers=_get_headers())
        # print "%s %s" % (url, str(response.status_code))
        if response.status_code == 200:
            print "Check or client is stashed"
            sys.exit(0)


def _create_trigger_type():
    try:
        url = _get_st2_triggers_url()
        payload = {
            'name': ST2_TRIGGERTYPE_NAME,
            'pack': ST2_TRIGGERTYPE_PACK,
            'description': 'Trigger type for sensu event handler.'
        }
        # sys.stdout.write('POST: %s: Body: %s\n' % (url, payload))
        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'

        if ST2_AUTH_TOKEN:
            headers['X-Auth-Token'] = ST2_AUTH_TOKEN

        post_resp = requests.post(url, data=json.dumps(payload),
                                  headers=headers, verify=False)
    except:
        sys.stderr.write('Unable to register trigger type with st2.')
        raise
    else:
        status = post_resp.status_code
        if status not in OK_CODES:
            sys.stderr.write('Failed to register trigger type with st2. \
                HTTP_CODE: %d\n' %
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
                             auth=(ST2_USERNAME, ST2_PASSWORD), verify=False)
    except:
        sys.stderr.write('Cannot get auth token from st2. Will try unauthed.')
    else:
        if resp.status_code not in OK_CODES:
            sys.stderr.write("Cannot authenticate. Will try unauthed.")
            return
        ST2_AUTH_TOKEN = resp.json()['token']


def _register_with_st2():
    global REGISTERED_WITH_ST2
    try:
        url = urljoin(_get_st2_triggers_url(), ST2_TRIGGERTYPE_REF)
        # sys.stdout.write('GET: %s\n' % url)
        if not ST2_AUTH_TOKEN:
            _get_auth_token()

        if ST2_AUTH_TOKEN:
            get_resp = requests.get(url, headers={'X-Auth-Token':
                                                  ST2_AUTH_TOKEN}, verify=False)
        else:
            get_resp = requests.get(url, verify=False)

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
    headers['X-ST2-Integration'] = 'sensu.'
    headers['Content-Type'] = 'application/json; charset=utf-8'
    if ST2_AUTH_TOKEN:
        headers['X-Auth-Token'] = ST2_AUTH_TOKEN
    try:
        # sys.stdout.write('POST: url: %s, body: %s\n' % (url, body))
        r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
    except:
        sys.stderr.write('Cannot connect to st2 endpoint.')
    else:
        status = r.status_code
        if status not in OK_CODES:
            sys.stderr.write('Failed posting sensu event to st2. HTTP_CODE: \
                %d\n' % status)
        else:
            sys.stdout.write('Sent sensu event to st2. HTTP_CODE: \
                %d\n' % status)


def main(args):
    body = {}
    body['trigger'] = ST2_TRIGGERTYPE_REF
    body['payload'] = json.loads(sys.stdin.read().strip())
    client = body['payload']['client']['name']
    check = body['payload']['check']['name']
    if not _check_stash(client, check):
        _post_event_to_st2(_get_st2_webhooks_url(), body)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        st2_config_file = sys.argv[1]
    else:
        sys.stderr.write('Error: config file missing.\n')
        sys.stderr.write('Usage: %s ST2_CONFIG_FILE\n' % sys.argv[0])
        exit(-1)

    try:
        if not os.path.exists(st2_config_file):
            sys.stderr.write('Configuration file not found. Exiting.\n')
            sys.exit(1)

        with open(st2_config_file) as f:
            config = yaml.safe_load(f)
            ST2_USERNAME = config['st2_username']
            ST2_PASSWORD = config['st2_password']
            ST2_API_BASE_URL = config['st2_api_base_url']
            ST2_AUTH_BASE_URL = config['st2_auth_base_url']
            SENSU_HOST = config.get('sensu_host', 'localhost')
            SENSU_PORT = config.get('sensu_port', '4567')
            SENSU_USER = config.get('sensu_user', None)
            SENSU_PASS = config.get('sensu_pass', None)

        if not REGISTERED_WITH_ST2:
            _register_with_st2()
    except Exception as e:
        sys.stderr.write(
            'Failed registering with st2. Won\'t post event.\n')
        sys.stderr.write(traceback.format_exc())
    else:
        main(sys.argv)
