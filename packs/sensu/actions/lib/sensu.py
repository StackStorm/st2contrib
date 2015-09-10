import base64
import json
import os
import requests

import yaml


def parseOutput(r):
    try:
        output = {}
        json.loads(r.text)
        for c in r.json():
            output[c['name']] = c
        return json.dumps(output)
    except:
        return r.text


class Sensu(object):

    def __init__(self, conf):

        config_file = os.path.join(os.path.dirname(__file__), conf)
        try:
            fh = open(config_file)
            self.config = yaml.safe_load(fh)
            fh.close()
        except Exception as e:
            print("Error reading config file %s: %s" % (conf, e))

        if self.config['ssl']:
            protocol = 'https'
        else:
            protocol = "http"
        self.config[
            'base_url'] = "%s://%s:%s" % (protocol, self.config['host'], self.config['port'])

    def get_headers(self):
        b64auth = base64.b64encode(
            "%s:%s" %
            (self.config['user'], self.config['pass']))
        auth_header = "BASIC %s" % b64auth
        content_header = "application/json"
        return {"Authorization": auth_header, "Content-Type": content_header}


class Aggregates(object):

    def __init__(self, conf):
        sensu = Sensu(conf)
        self.headers = sensu.get_headers()
        self.url = "%s/aggregates" % sensu.config['base_url']

    def list(self, limit=None, offset=None):
        data = {}
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return parseOutput(
            requests.get(
                url=self.url,
                headers=self.headers,
                data=data))

    def check(self, check, age=None):
        data = {}
        self.url = "%s/%s" % (self.url, check)
        if age:
            data['age'] = age
        return parseOutput(
            requests.get(
                url=self.url,
                headers=self.headers,
                data=data))

    def delete(self, check):
        self.url = "%s/%s" % (self.url, check)
        return parseOutput(requests.delete(url=self.url, headers=self.headers))

    def check_issued(self, check, issued, summarize=None, results=None):
        data = {}
        self.url = "%s/%s/%s" % (self.url, check, issued)
        if summarize:
            data['summarize'] = summarize
        if results:
            data['results'] = results
        return parseOutput(
            requests.get(
                url=self.url,
                headers=self.headers,
                data=data))


class Checks(object):

    def __init__(self, conf):
        self.sensu = Sensu(conf)
        self.headers = self.sensu.get_headers()
        self.url = "%s/checks" % self.sensu.config['base_url']

    def list(self):
        return parseOutput(requests.get(url=self.url, headers=self.headers))

    def get(self, check):
        url = "%s/%s" % (self.url, check)
        return parseOutput(requests.get(url=url, headers=self.headers))

    def request(self, check, subscribers):
        url = "%s/request" % self.sensu.config['base_url']
        payload = {}
        subs = []
        if not isinstance(subscribers, list):
            subs.append(subscribers)
        payload['check'] = check
        payload['subscribers'] = subscribers
        return parseOutput(
            requests.post(
                url=url,
                headers=self.headers,
                data=payload))


class Clients(object):

    def __init__(self, conf):
        sensu = Sensu(conf)
        self.headers = sensu.get_headers()
        self.url = "%s/clients" % sensu.config['base_url']

    def list(self, limit=None, offset=None):
        data = {}
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return parseOutput(
            requests.get(
                url=self.url,
                headers=self.headers,
                data=data))

    def get(self, client):
        url = "%s/%s" % (self.url, client)
        return parseOutput(requests.get(url=url, headers=self.headers))

    def delete(self, client):
        url = "%s/%s" % (self.url, client)
        return parseOutput(requests.delete(url=url, headers=self.headers))

    def history(self, client):
        url = "%s/%s/history" % (self.url, client)
        return parseOutput(requests.get(url=url, headers=self.headers))


class Stashes(object):

    def __init__(self, conf):
        sensu = Sensu(conf)
        self.headers = sensu.get_headers()
        self.url = "%s/stashes" % sensu.config['base_url']

    def list(self, limit, offset):
        data = {}
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset
        return parseOutput(
            requests.get(
                url=self.url,
                headers=self.headers,
                data=data))

    def get(self, stash):
        url = "%s/%s" % (self.url, stash)
        return parseOutput(requests.get(url=url, headers=self.headers))

    def delete(self, stash):
        url = "%s/%s" % (self.url, stash)
        return parseOutput(requests.delete(url=url, headers=self.headers))

    def post(self, data):
        return parseOutput(
            requests.post(
                url=self.url,
                headers=self.headers,
                data=data))

    def post_by_path(self, path, data):
        url = "%s/%s" % (self.url, path)
        return parseOutput(
            requests.post(
                url=url,
                headers=self.headers,
                data=data))


class Status(object):

    def __init__(self, conf):
        sensu = Sensu(conf)
        self.headers = sensu.get_headers()
        self.url = sensu.config['base_url']

    def health(self, consumers=2, messages=100):
        url = "%s/health" % self.url
        data = {'consumers': consumers, 'messages': messages}
        return parseOutput(
            requests.get(
                url=url,
                headers=self.headers,
                data=data))

    def info(self):
        url = "%s/info" % self.url
        return parseOutput(requests.get(url=url, headers=self.headers))


class Events(object):

    def __init__(self, conf):
        self.sensu = Sensu(conf)
        self.headers = self.sensu.get_headers()
        self.url = "%s/events" % self.sensu.config['base_url']

    def list_all(self):
        return parseOutput(requests.get(url=self.url, headers=self.headers))

    def list_by_client(self, client):
        url = "%s/%s" % (self.url, client)
        return parseOutput(requests.get(url=url, headers=self.headers))

    def get(self, client, check):
        url = "%s/%s/%s" % (self.url, client, check)
        return parseOutput(requests.get(url=url, headers=self.headers))

    def delete(self, client, check):
        url = "%s/%s/%s" % (self.url, client, check)
        return parseOutput(requests.delete(url=url, headers=self.headers))

    def resolve(self, client, check):
        url = "%s/resolve" % self.sensu['base_url']
        payload = {'client': client, 'check': check}
        return parseOutput(
            requests.post(
                url=url,
                headers=self.headers,
                data=payload))
