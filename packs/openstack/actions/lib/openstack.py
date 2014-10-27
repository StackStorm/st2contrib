import os
import re
import json
import types
from keystoneclient.auth.identity import v2
from keystoneclient import session
from keystoneclient.v2_0.client import Client as keyclient


class OpenStack(object):

    def __init__(self, conf):

        config_file = os.path.join(os.path.dirname(__file__), '../', conf)
        try:
            fh = open(config_file)
            config = json.load(fh)
            fh.close()
        except Exception as e:
            print("Error reading config file %s: %s" % (conf, e))

        self.username = config['username']
        self.password = config['password']
        self.tenant = config['tenant']
        self.auth_url = config['auth_url']
        self.endpoints = config['endpoints']
        self.act_name = ""

    def getSession(self):
        self.auth = v2.Password(auth_url=self.auth_url,
                                username=self.username,
                                password=self.password,
                                tenant_name=self.tenant)

        return session.Session(auth=self.auth)

    def getToken(self):
        session = self.getSession()
        return session.get_token()

    def getEndpoint(self, service):
        token = self.getToken()
        client = keyclient(auth_url=self.auth_url, token=token)
        print(client.services.list())

    def parseAction(self, instance, parts):
        args, parts = self.parseArgs(parts)
        foo = None
        try:
            self.act_name = parts[0]
            foo = getattr(instance, self.act_name)
        except AttributeError:
            print("That look like an incorrect tiddly bit.")
        else:
            parts.pop(0)
            for p in parts:
                try:
                    foo = getattr(foo, p)
                except AttributeError:
                    print("That tiddly bit be wrong")
        return foo, args

    def parseOutput(self, output):
        results = {self.act_name: []}

        if hasattr(
                output,
                '__getitem__') or isinstance(
                output,
                types.GeneratorType):
            for result in output:
                if hasattr(result, 'to_dict'):
                    result = result.to_dict()
                results[self.act_name].append(result)
        else:
            if hasattr(output, 'to_dict'):
                results[self.act_name] = output.to_dict()
            else:
                results[self.act_name] = output
        return results

    def run(self, instance, parts):
        action, args = self.parseAction(instance, parts)

        return self.parseOutput(action(**args))

    def parseArgs(self, arg):
        arg.pop(0)
        args = {}
        parts = []
        for a in arg:
            if re.search('=', a):
                argsplit = a.split('=')
                args[argsplit[0]] = argsplit[1]
            else:
                parts.append(a)
        return args, parts
