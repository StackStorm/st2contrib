#!/usr/bin/env python

import argparse
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

ST2_API_BASE_URL = 'https://localhost/v1/'
ST2_USERNAME = None
ST2_PASSWORD = None
ST2_AUTH_TOKEN = None

ST2_AUTH_PATH = 'auth/tokens'
ST2_WEBHOOKS_PATH = 'api/webhooks/st2/'
ST2_TRIGGERS_PATH = 'api/triggertypes/'
ST2_TRIGGERTYPE_PACK = 'sensu'
ST2_TRIGGERTYPE_NAME = 'event_handler'
ST2_TRIGGERTYPE_REF = '.'.join([ST2_TRIGGERTYPE_PACK, ST2_TRIGGERTYPE_NAME])

# Sensu configuration

SENSU_HOST = 'localhost'
SENSU_PORT = 4567
SENSU_USER = ''
SENSU_PASS = ''

REGISTERED_WITH_ST2 = False
UNAUTHED = False

OK_CODES = [httplib.OK, httplib.CREATED, httplib.ACCEPTED, httplib.CONFLICT]
UNREACHABLE_CODES = [httplib.NOT_FOUND]


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


def _create_trigger_type(verbose=False):
    try:
        url = _get_st2_triggers_url()
        payload = {
            'name': ST2_TRIGGERTYPE_NAME,
            'pack': ST2_TRIGGERTYPE_PACK,
            'description': 'Trigger type for sensu event handler.'
        }

        headers = {}
        headers['Content-Type'] = 'application/json; charset=utf-8'

        if ST2_AUTH_TOKEN:
            headers['X-Auth-Token'] = ST2_AUTH_TOKEN

        if verbose:
            print('POST to URL %s for registering trigger. Body = %s, headers = %s.' %
                  (url, payload, headers))
        post_resp = requests.post(url, data=json.dumps(payload),
                                  headers=headers, verify=False)
    except:
        traceback.print_exc(limit=20)
        raise Exception('Unable to connect to st2 endpoint %s.' % url)
    else:
        status = post_resp.status_code
        if status in UNREACHABLE_CODES:
            msg = 'Got response %s. Invalid triggers endpoint %s. Check configuration!' % (
                status,
                url
            )
            raise Exception(msg)

        if status not in OK_CODES:
            msg = 'Failed to register trigger type %s.%s with st2. HTTP_CODE: %s' % (
                ST2_TRIGGERTYPE_PACK, ST2_TRIGGERTYPE_NAME, status
            )
            raise Exception(msg)
        else:
            print('Registered trigger type with st2.')


def _get_auth_url():
    return urljoin(ST2_API_BASE_URL, ST2_AUTH_PATH)


def _get_auth_token(verbose=False):
    auth_url = _get_auth_url()

    if verbose:
        print('Will POST to URL %s to get auth token.' % auth_url)

    try:
        resp = requests.post(auth_url, json.dumps({'ttl': 5 * 60}),
                             auth=(ST2_USERNAME, ST2_PASSWORD), verify=False)
    except:
        traceback.print_exc(limit=20)
        raise Exception('Unable to connect to st2 endpoint %s.' % auth_url)
    else:
        if resp.status_code in UNREACHABLE_CODES:
            msg = 'Got response %s. Invalid auth endpoint %s. Check configuration!' % (
                resp.status_code,
                auth_url
            )
            raise Exception(msg)
        if resp.status_code not in OK_CODES:
            msg = 'Cannot get a valid auth token from %s. HTTP_CODE: %s' % (
                auth_url,
                resp.status_code
            )
            raise Exception(msg)
        return resp.json()['token']


def _register_trigger_with_st2(verbose=False):
    global REGISTERED_WITH_ST2
    global ST2_AUTH_TOKEN
    triggers_url = urljoin(_get_st2_triggers_url(), ST2_TRIGGERTYPE_REF)

    if verbose:
        print('Unauthed? : %s' % UNAUTHED)

    if not UNAUTHED:
        try:
            if not ST2_AUTH_TOKEN:
                if verbose:
                    print('No auth token found. Let\'s get one from StackStorm!')
                ST2_AUTH_TOKEN = _get_auth_token(verbose=verbose)
        except:
            raise Exception('Unable to negotiate an auth token. Exiting!')

    try:
        if verbose:
            print('Will GET from URL %s for detecting trigger %s.' % (
                  triggers_url, ST2_TRIGGERTYPE_REF))

        if ST2_AUTH_TOKEN:
            get_resp = requests.get(triggers_url, headers={'X-Auth-Token':
                                    ST2_AUTH_TOKEN}, verify=False)
        else:
            if verbose:
                print('Resorting to unauthed requests to register trigger type.')
            get_resp = requests.get(triggers_url, verify=False)

        if get_resp.status_code != httplib.OK:
            _create_trigger_type(verbose=verbose)
        else:
            body = json.loads(get_resp.text)
            if len(body) == 0:
                _create_trigger_type(verbose=verbose)
    except:
        traceback.print_exc(limit=20)
        raise Exception('Unable to connect to st2 endpoint %s.' % triggers_url)
    else:
        if verbose:
            print('Successfully registered trigger %s with st2.' % ST2_TRIGGERTYPE_REF)

        REGISTERED_WITH_ST2 = True


def _get_st2_triggers_url():
    url = urljoin(ST2_API_BASE_URL, ST2_TRIGGERS_PATH)
    return url


def _get_st2_webhooks_url():
    url = urljoin(ST2_API_BASE_URL, ST2_WEBHOOKS_PATH)
    return url


def _post_webhook(url, body, verbose):
    headers = {}
    headers['X-ST2-Integration'] = 'sensu.'
    headers['St2-Trace-Tag'] = body['payload']['id']
    headers['Content-Type'] = 'application/json; charset=utf-8'
    if ST2_AUTH_TOKEN:
        headers['X-Auth-Token'] = ST2_AUTH_TOKEN
    try:
        if verbose:
            print('Webhook POST: url: %s, body: %s\n' % (url, body))
        r = requests.post(url, data=json.dumps(body), headers=headers, verify=False)
    except:
        raise Exception('Cannot connect to st2 endpoint %s.' % url)
    else:
        status = r.status_code

        if status in UNREACHABLE_CODES:
            msg = 'Webhook URL %s does not exist. Check if you have a rule registered for ' + \
                  'trigger with st2. st2 rule list --trigger=%s' % ST2_TRIGGERTYPE_REF
            raise Exception(msg)

        if status not in OK_CODES:
            sys.stderr.write('Failed posting sensu event to st2. HTTP_CODE: \
                %d\n' % status)
        else:
            sys.stdout.write('Sent sensu event to st2. HTTP_CODE: \
                %d\n' % status)


def _post_event_to_st2(payload, verbose=False):
    body = {}
    body['trigger'] = ST2_TRIGGERTYPE_REF

    try:
        body['payload'] = json.loads(payload.strip())
    except:
        print('Invalid JSON payload %s.' % payload)
        sys.exit(3)

    try:
        client = body['payload']['client']['name']
        check = body['payload']['check']['name']
    except KeyError:
        print('Invalid payload spec %s.' % payload)

    if not _check_stash(client, check):
        try:
            _post_event_to_st2(_get_st2_webhooks_url(), body, verbose=verbose)
        except:
            traceback.print_exc(limit=20)
            print('Cannot send event to st2.')
            sys.exit(4)


def _register_with_st2(verbose=False):
    try:
        if not REGISTERED_WITH_ST2:
            if verbose:
                print('Checking if trigger %s registered with st2.' % ST2_TRIGGERTYPE_REF)
            _register_trigger_with_st2(verbose=verbose)
    except:
        traceback.print_exc(limit=20)
        sys.stderr.write(
            'Failed registering with st2. Won\'t post event.\n')
        sys.exit(2)


def _set_config_opts(config_file, verbose=False, unauthed=False):
    global ST2_USERNAME
    global ST2_PASSWORD
    global ST2_API_BASE_URL
    global SENSU_HOST
    global SENSU_PORT
    global SENSU_USER
    global SENSU_PASS
    global UNAUTHED

    UNAUTHED = unauthed

    if not os.path.exists(config_file):
        print('Configuration file %s not found. Exiting!!!' % config_file)
        sys.exit(1)

    with open(config_file) as f:
        config = yaml.safe_load(f)

        if verbose:
            print('Contents of config file: %s' % config)

        ST2_USERNAME = config['st2_username']
        ST2_PASSWORD = config['st2_password']
        ST2_API_BASE_URL = config['st2_api_base_url']
        SENSU_HOST = config.get('sensu_host', 'localhost')
        SENSU_PORT = config.get('sensu_port', '4567')
        SENSU_USER = config.get('sensu_user', None)
        SENSU_PASS = config.get('sensu_pass', None)


def main(config_file, payload, verbose=False, unauthed=False):
    _set_config_opts(config_file=config_file, unauthed=unauthed, verbose=verbose)
    _register_with_st2(verbose=verbose)
    _post_event_to_st2()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='StackStorm sensu event handler.')
    parser.add_argument('config_path',
                        help='Exchange to listen on')
    parser.add_argument('--verbose', '-v', required=False, action='store_true',
                        help='Verbose mode.')
    parser.add_argument('--unauthed', '-u', required=False, action='store_true',
                        help='Allow to post to unauthed st2. E.g. when auth is disabled ' +
                        'server side.')
    args = parser.parse_args()
    payload = sys.stdin.read().strip()
    main(config_file=args.config_path, payload=payload, verbose=args.verbose,
         unauthed=args.unauthed)
