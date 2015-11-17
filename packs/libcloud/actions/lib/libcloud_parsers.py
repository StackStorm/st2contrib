#!/usr/bin/env python

import libcloud.compute.base as compute_base
import libcloud.dns.base as dns_base
import libcloud.loadbalancer.base as lb_base

__all__ = [
    'FieldLists',
    'ResultSets'
]


class FieldLists(object):
    """
    The lists of fields we want to return for each class
    """
    NODE = ['id', 'name', 'state', 'public_ips', 'private_ips', 'size', 'image']
    NODE_SIZE = ['id', 'name', 'ram', 'disk', 'bandwidth', 'price']
    NODE_IMAGE = ['id', 'name']
    LOCATION = ['id', 'name', 'country']
    NODE_KEY = ['pubkey']
    NODE_PASSWORD = ['password', 'generated']
    STORAGE_VOLUME = ['id', 'name', 'size', 'state']
    VOLUME_SNAPSHOT = ['id', 'size', 'state']
    ZONE = ['id', 'domain', 'type', 'ttl']
    RECORD = ['id', 'name', 'type', 'data', 'zone']
    MEMBER = ['id', 'ip', 'port', 'balancer']
    BALANCER = ['id', 'name', 'state', 'port']


class ResultSets(object):

    def selector(self, output):
        if isinstance(output, compute_base.Node):
            return self.parse(output, FieldLists.NODE)
        elif isinstance(output, compute_base.NodeSize):
            return self.parse(output, FieldLists.NODE_SIZE)
        elif isinstance(output, compute_base.NodeImage):
            return self.parse(output, FieldLists.NODE_IMAGE)
        elif isinstance(output, compute_base.NodeLocation):
            return self.parse(output, FieldLists.LOCATION)
        elif isinstance(output, compute_base.NodeAuthSSHKey):
            return self.parse(output, FieldLists.NODE_KEY)
        elif isinstance(output, compute_base.NodeAuthPassword):
            return self.parse(output, FieldLists.NODE_PASSWORD)
        elif isinstance(output, compute_base.StorageVolume):
            return self.parse(output, FieldLists.STORAGE_VOLUME)
        elif isinstance(output, compute_base.VolumeSnapshot):
            return self.parse(output, FieldLists.VOLUME_SNAPSHOT)
        elif isinstance(output, dns_base.Zone):
            return self.parse(output, FieldLists.ZONE)
        elif isinstance(output, dns_base.Record):
            return self.parse(output, FieldLists.RECORD)
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
