#!/usr/bin/env python

import libcloud.common.dimensiondata as dd
import libcloud.compute.base as base
import libcloud.loadbalancer.base as lb_base


class FieldLists():
    STATUS = ['action', 'request_time', 'user_name',
              'number_of_steps', 'update_time', 'step_name',
              'step_number', 'step_percent_complete', 'failure_reason']
    NETWORK = ['id', 'name', 'description', 'private_net',
               'multicast', 'status']
    NETWORK_DOMAIN = ['id', 'name', 'description', 'plan', 'status']
    VLAN = ['id', 'name', 'description', 'private_ipv4_range_address',
            'status', 'private_ipv4_range_size', 'network_domain',
            'ipv6_range_address', 'ipv6_range_size', 'ipv4_gateway',
            'ipv6_gateway']
    NODE = ['id', 'name', 'state', 'public_ips', 'private_ips', 'image']
    VIP_NODE = ['id', 'name', 'status', 'ip']
    NODE_IMAGE = ['id', 'name']
    LOCATION = ['id', 'name', 'country']
    FIREWALL_RULE = ['id', 'name', 'action', 'ip_version', 'protocol',
                     'enabled', 'source', 'destination', 'status', 'network_domain']
    FIREWALL_RULE_ADDRESS = ['any_ip', 'ip_address', 'ip_prefix_size',
                             'port_begin', 'port_end']
    NAT_RULE = ['id', 'internal_ip', 'external_ip', 'status']
    IP_BLOCK = ['id', 'base_ip', 'size', 'status', 'network_domain']
    MEMBER = ['id', 'ip', 'port', 'balancer']
    BALANCER = ['id', 'name', 'state', 'port']


class ResultSets(object):

    def selector(self, output):
        if isinstance(output, dd.DimensionDataNetwork):
            return self.parse(output, FieldLists.NETWORK)
        elif isinstance(output, dd.DimensionDataNetworkDomain):
            return self.parse(output, FieldLists.NETWORK_DOMAIN)
        elif isinstance(output, dd.DimensionDataFirewallRule):
            return self.parse(output, FieldLists.FIREWALL_RULE)
        elif isinstance(output, dd.DimensionDataFirewallAddress):
            return self.parse(output, FieldLists.FIREWALL_RULE_ADDRESS)
        elif isinstance(output, dd.DimensionDataVIPNode):
            return self.parse(output, FieldLists.VIP_NODE)
        elif isinstance(output, dd.DimensionDataPublicIpBlock):
            return self.parse(output, FieldLists.IP_BLOCK)
        elif isinstance(output, dd.DimensionDataNatRule):
            return self.parse(output, FieldLists.NAT_RULE)
        elif isinstance(output, dd.DimensionDataStatus):
            return self.parse(output, FieldLists.STATUS)
        elif isinstance(output, dd.DimensionDataVlan):
            return self.parse(output, FieldLists.VLAN)
        elif isinstance(output, base.Node):
            return self.parse(output, FieldLists.NODE)
        elif isinstance(output, base.NodeImage):
            return self.parse(output, FieldLists.NODE_IMAGE)
        elif isinstance(output, base.NodeLocation):
            return self.parse(output, FieldLists.LOCATION)
        elif isinstance(output, lb_base.Member):
            return self.parse(output, FieldLists.MEMBER)
        elif isinstance(output, lb_base.LoadBalancer):
            return self.parse(output, FieldLists.BALANCER)
        else:
            return output

    def formatter(self, output):
        formatted = []
        if isinstance(output, list):
            for o in output:
                formatted.append(self.selector(o))
        else:
            formatted = self.selector(output)
        return formatted

    def _getval(self, obj, field):
        return self.selector(getattr(obj, field))

    def parse(self, output, field_list):
        instance_data = {field: self._getval(output, field) for field in field_list}
        return instance_data
