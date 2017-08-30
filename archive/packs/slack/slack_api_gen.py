import yaml
import re
import urllib2
from bs4 import BeautifulSoup

method_dict = {}
base_url = 'https://api.slack.com/methods'

api_doc_main = urllib2.urlopen('%s/channels.invite' % base_url)

soup = BeautifulSoup(api_doc_main)

api_methods = soup.find('select', id='api_method')

for method in api_methods.stripped_strings:
    if method != 'View another method...':
        method_dict[method] = {'params': {}}
        method_url = "%s/%s" % (base_url, method)
        method_page = urllib2.urlopen(method_url)
        method_soup = BeautifulSoup(method_page)
        method_description = method_soup.find('section', attrs={
            "class": "tab_pane selected clearfix large_bottom_padding"}) \
            .find_all('p')[0].text
        method_description = re.sub('\n|\r', ' ', method_description)
        method_dict[method]['description'] = method_description
        method_args_table = method_soup.find('table', attrs={
            "class": "arguments full_width"}).tbody.find_all('tr')
        del method_args_table[0]
        for row in method_args_table:
            arg = row.find('code')
            required = row.find_all('td')[2]
            if re.search("Required", required.text):
                required = True
                default = None
            elif re.search(",", required.text):
                required, default = required.text.split(',')
                required = False
                default = default.split('=')[1]
            else:
                required = False
                default = None
            method_dict[method]['params'][arg.text] = {}
            method_dict[method]['params'][arg.text]['required'] = required
            method_dict[method]['params'][arg.text]['default'] = default

for method in method_dict:

    file_name = 'actions/%s.yaml' % method
    output_dict = {'name': method,
                   'runner_type': 'run-python',
                   'enabled': True,
                   'entry_point': 'run.py',
                   'description': method_dict[method]['description'],
                   'parameters': {
                       'end_point': {
                           'type': 'string',
                           'immutable': True,
                           'default': method}
                   }
                   }

    for param in method_dict[method]['params']:
        if param == 'token':
            method_dict[method]['params'][param]['required'] = False
        output_dict['parameters'][param] = {'type': 'string'}
        if method_dict[method]['params'][param]['default'] is not None:
            output_dict['parameters'][param]['default'] = \
                method_dict[method]['params'][param]['default']
        output_dict['parameters'][param]['required'] = \
            method_dict[method]['params'][param]['required']

    print yaml.safe_dump(output_dict, default_flow_style=False)
    fh = open(file_name, 'w')
    fh.write(yaml.safe_dump(output_dict, default_flow_style=False))
    fh.close()
