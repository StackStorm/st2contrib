#!/usr/bin/env python

# Requirements
# pip install jira

try:
    import simplejson as json
except ImportError:
    import json
import os, argparse
import sys

from jira.client import JIRA

CONFIG_FILE = os.path.join(os.path.dirname(__file__),'lib/jira_config.json')


class AuthedJiraClient(object):
    def __init__(self, jira_server, oauth_creds):
        self._client = JIRA(options={'server': jira_server},
                            oauth=oauth_creds)

    def is_project_exists(self, project):
        projs = self._client.projects()
        project_names = [proj.key for proj in projs]
        if project not in project_names:
            return False
        return True

    def create_issue(self, project=None, summary=None, desc=None, issuetype=None):
        issue_dict = {
            'project': {'key': project},
            'summary': summary,
            'description': desc,
            'issuetype': {'name': issuetype},
        }
        new_issue = self._client.create_issue(fields=issue_dict)
        return new_issue


def _read_cert(file_path):
    with open(file_path) as f:
        return f.read()


def _parse_args():

    parser = argparse.ArgumentParser(description='Create a new Jira Issue')
    parser.add_argument('--project_name', help='Jira Project Name', default="DEMO")
    parser.add_argument('--issue_summary', help='Brief Issue Summary')
    parser.add_argument('--issue_description', help='Full Issue Description')
    parser.add_argument('--issue_type', help='Type of Issue')
    args = parser.parse_args()

    return args


def _get_jira_client(config):
    rsa_cert_file = config['rsa_cert_file']
    if not os.path.exists(rsa_cert_file):
        raise Exception('Cert file for JIRA OAuth not found at %s.' % rsa_cert_file)
    rsa_key = _read_cert(rsa_cert_file)
    oauth_creds = {
        'access_token': config['oauth_token'],
        'access_token_secret': config['oauth_token_secret'],
        'consumer_key': config['consumer_key'],
        'key_cert': rsa_key
    }
    jira_client = AuthedJiraClient(config['jira_server'], oauth_creds)
    return jira_client


def _get_config():
    global CONFIG_FILE
    if not os.path.exists(CONFIG_FILE):
        raise Exception('Config file not found at %s.' % CONFIG_FILE)
    with open(CONFIG_FILE) as f:
        return json.load(f)


def main(args):
    cfg = _get_config()
    try:
        client = _get_jira_client(cfg)
    except Exception as e:
        sys.stderr.write('Failed to create JIRA client: %s\n' % str(e))
        sys.exit(1)

    params = _parse_args()
    proj = params.project_name
    try:
        if not client.is_project_exists(proj):
            raise Exception('Project ' + proj + ' does not exist.')
        issue = client.create_issue(project=params.project_name,
                                    summary=params.issue_summary,
                                    desc=params.issue_description,
                                    issuetype=params.issue_type)
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        sys.exit(2)
    else:
        sys.stdout.write('Issue ' + str(issue) + ' created.\n')

if __name__ == '__main__':
    main(sys.argv)
