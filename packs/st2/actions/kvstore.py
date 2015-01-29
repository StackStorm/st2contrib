from st2actions.runners.pythonrunner import Action
from st2client.client import Client
from st2client.models.datastore import KeyValuePair


class KVPAction(Action):

    def run(self, key, action, st2host='localhost', value=""):
        st2_endpoints = {
            'action': "http://%s:9101" % st2host,
            'reactor': "http://%s:9102" % st2host,
            'datastore': "http://%s:9103" % st2host
        }

        try:
            client = Client(st2_endpoints)
        except Exception as e:
            return e

        if action == 'get':
            kvp = client.keys.get_by_name(key)

            if not kvp:
                raise Exception('Key error with %s.' % key)

            return kvp.value
        else:
            instance = KeyValuePair()
            if action == 'create':
                instance.id = key
            else:
                instance.id = client.keys.get_by_name(key).id
            instance.name = key
            instance.value = value

            try:
                kvstore = getattr(client.keys, action)
                kvp = kvstore(instance)
            except Exception as e:
                raise

            if action == 'delete':
                return kvp
            else:
                return kvp.serialize()
