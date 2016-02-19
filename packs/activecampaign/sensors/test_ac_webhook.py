import requests
import json
import yaml
import os

ACTION = "my_action"

config_yaml = os.path.join(os.path.dirname(__file__), '../config.yaml')
conf = yaml.load(open(config_yaml))

url = 'http://localhost:{}/{}/{}'.format(
    conf['webhook']['port'], conf['webhook']['path'], ACTION)
print "Posting to %s..." % url

headers = {
    'X-Google-Apps-Metadata':  'domain=mockable.io,host=*.mockable.io',
    'X-Appengine-Citylatlong':  '33.835293,-117.914504',
    'Content_Type': 'application/x-www-form-urlencoded',
    'Content-Type': 'application/x-www-form-urlencoded',
}
data = "contact%5Bid%5D=903&contact%5Bemail%5D=ivan%40grozny.me&contact%5Bfirst_name%5D=Ivan&contact%5Blast_name%5D=Grozny&contact%5Bphone%5D=&contact%5Borgname%5D=&contact%5Bip4%5D=69.181.118.28&contact%5Bfields%5D%5Beula%5D=%7C%7CYes%2C+I+agree+to+the+terms+of+EULA%7C%7C&seriesid=22"
response = requests.post(url, data=data, headers=headers)
print json.dumps(response.json(), indent=4)
