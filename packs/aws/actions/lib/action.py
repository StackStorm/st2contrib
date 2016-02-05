import re
import eventlet
import importlib

import boto.ec2
import boto.route53
import boto.vpc

from st2actions.runners.pythonrunner import Action
from ec2parsers import ResultSets


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config['st2_user_data'] is not "":
            self.userdata = open(config['st2_user_data'], 'r').read()
        else:
            self.userdata = None
        self.setup = config['setup']
        self.resultsets = ResultSets()

    def ec2_connect(self):
        region = self.setup['region']
        del self.setup['region']
        return boto.ec2.connect_to_region(region, **self.setup)

    def vpc_connect(self):
        region = self.setup['region']
        del self.setup['region']
        return boto.vpc.connect_to_region(region, **self.setup)

    def r53_connect(self):
        del self.setup['region']
        return boto.route53.connection.Route53Connection(**self. setup)

    def get_r53zone(self, zone):
        conn = self.r53_connect()
        return conn.get_zone(zone)

    def st2_user_data(self):
        return self.userdata

    def split_tags(self, tags):
        tag_dict = {}
        split_tags = tags.split(',')
        for tag in split_tags:
            if re.search('=', tag):
                k, v = tag.split('=', 1)
                tag_dict[k] = v
        return tag_dict

    def wait_for_state(self, instance_id, state, timeout=10, retries=3):
        state_list = {}
        obj = self.ec2_connect()
        eventlet.sleep(timeout)
        instance_list = []

        for _ in range(retries + 1):
            try:
                instance_list = obj.get_only_instances([instance_id, ])
            except Exception:
                self.logger.info("Waiting for instance to become available")
                eventlet.sleep(timeout)

        for instance in instance_list:
            try:
                current_state = instance.update()
            except Exception, e:
                self.logger.info("Instance (%s) not listed. Error: %s" %
                                 (instance_id, e))
                eventlet.sleep(timeout)

            while current_state != state:
                current_state = instance.update()
            state_list[instance_id] = current_state
        return state_list

    def do_method(self, module_path, cls, action, **kwargs):
        module = importlib.import_module(module_path)
        # hack to connect to correct region
        if cls == 'EC2Connection':
            obj = self.ec2_connect()
        elif cls == 'VPCConnection':
            obj = self.vpc_connect()
        elif module_path == 'boto.route53.zone' and cls == 'Zone':
            zone = kwargs['zone']
            del kwargs['zone']
            obj = self.get_r53zone(zone)
        else:
            del self.setup['region']
            obj = getattr(module, cls)(**self.setup)
        resultset = getattr(obj, action)(**kwargs)
        formatted = self.resultsets.formatter(resultset)
        return formatted if isinstance(formatted, list) else [formatted]

    def do_function(self, module_path, action, **kwargs):
        module = __import__(module_path)
        return getattr(module, action)(**kwargs)
