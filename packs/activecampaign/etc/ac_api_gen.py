import yaml
import re
import urllib2
from bs4 import BeautifulSoup

import sys
import time
import pprint

method_list = []
method_dict = {}
base_overview_url = 'http://www.activecampaign.com/api/overview.php'
base_example_url = 'http://www.activecampaign.com/api/example.php'

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
api_doc_main = opener.open(base_overview_url)

soup = BeautifulSoup(api_doc_main, 'html5lib')
api_containers = soup.find_all('div',{"class": "ac_api-container"})

for api_container in api_containers:
    methods = api_container.find_all('a')
    for method in methods:
        method_list.append(method.text)

for method in method_list:
    if method != 'View another method...':
        method_dict[method] = {'params':{}}
        method_url = '%s?call=%s' % (base_example_url, method)
        method_opener = urllib2.build_opener()
        method_opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        method_page = method_opener.open(method_url)
        method_soup = BeautifulSoup(method_page, 'html5lib')
        method_description = method_soup.find_all('h3')[0].text
        method_description = re.sub('\n|\r', ' ', method_description)
        method_dict[method]['description'] = method_description
        method_args_table = method_soup.find_all('table', {"class":"innertable"})
        if len(method_args_table) < 2 or method_args_table is None:
            print "skipping innertables..."
            continue
        method_args_table_rows = method_args_table[0].find_all('tr')
        del method_args_table_rows[0]
        for row in method_args_table_rows:
            required = False
            default = None
            param_type = 'string'
            param_parts = row.find_all('td')
            param_name = param_parts[0].text
            param_description = re.sub('\n|\r', ' ', param_parts[1].text)
            if '*' in param_name:
                required = True
                param_name = param_name[:-1]
            if '[' in param_name:
                param_type = 'object'
                param_name = param_name.split('[')[0]
            if param_name == 'p':
                default = {}
                required = False
            if param_name == 'api_output':
                default = 'json'
            if param_name == 'api_action':
                default = method
                required = False
            if param_name == 'api_key':
                required = False
            method_dict[method]['params'][param_name] = {'type':'string'}
            method_dict[method]['params'][param_name]['description'] = param_description
            method_dict[method]['params'][param_name]['required'] = required
            method_dict[method]['params'][param_name]['default'] = default
            method_dict[method]['params'][param_name]['type'] = param_type
    time.sleep(1)

for method in method_dict:

    file_name = 'actions/%s.yaml' % method
    output_dict = { 'name': method,
                    'runner_type': 'run-python',
                    'enabled': True,
                    'entry_point': 'run.py',
                    'description': method_dict[method]['description'],
                    'parameters': {}
                  }

    for param in method_dict[method]['params']:
        if param == 'token':
            method_dict[method]['params'][param]['required'] = False
        output_dict['parameters'][param] = {'type': method_dict[method]['params'][param]['type']}
        if method_dict[method]['params'][param]['default'] is not None:
            output_dict['parameters'][param]['default'] = method_dict[method]['params'][param]['default']
        output_dict['parameters'][param]['required'] = method_dict[method]['params'][param]['required']
        output_dict['parameters'][param]['description'] = method_dict[method]['params'][param]['description']

    print yaml.safe_dump(output_dict, default_flow_style=False)
    fh = open(file_name, 'w')
    fh.write(yaml.safe_dump(output_dict, default_flow_style=False))
    fh.close()
