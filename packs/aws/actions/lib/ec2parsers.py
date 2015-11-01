#!/usr/bin/env python

import boto
import six
#import boto.ec2
#import boto.route53
#import boto.s3
#import boto.vpc

class FieldLists():
    ADDRESS = ['public_ip', 'instance_id', 'domain', 'allocation_id', 'association_id',
               'network_interface_id', 'network_interface_owner_id', 'private_ip_address']
    BUCKET = ["LoggingGroup", "connection", "creation_date", "name"]
    INSTANCE = ['id', 'public_dns_name', 'private_dns_name', 'state', 'state_code',
                'previous_state', 'previous_state_code', 'key_name', 'instance_type',
                'launch_time', 'image_id', 'placement', 'placement_group', 'placement_tenancy',
                'kernel', 'ramdisk', 'architecture', 'hypervisor', 'virtualization_type',
                'ami_launch_index', 'monitored', 'monitoring_state', 'spot_instance_request_id',
                'subnet_id', 'vpc_id', 'private_ip_address', 'ip_address', 'platform',
                'root_device_name', 'root_device_type', 'state_reason']
    VOLUME = ['id', 'create_time', 'status', 'size', 'snapshot_id', 'zone', 'type', 'iops',
              'encrypted']
    EC2ZONE = ['name', 'state', 'region_name', 'messages']
    RECORD = ['alias_dns_name', 'alias_evaluate_target_health', 'alias_hosted_zone_id', 'failover',
              'health_check', 'identifier', 'name', 'region', 'resource_records', 'ttl', 'type',
              'weight']
    R53ZONE = ['callerreference', 'config', 'id', 'name', 'resourcerecordsetcount']
    R53STATUS = ['comment', 'id', 'status', 'submittedat']


class ResultSets(object):

    def __init__(self):
        self.foo = ""

    def selector(self, output):
        if isinstance(output, boto.ec2.instance.Reservation):
            return self.parseReservation(output)
        elif isinstance(output, boto.ec2.instance.Instance):
            return self.parseInstance(output)
        elif isinstance(output, boto.ec2.volume.Volume):
            return self.parseVolume(output)
        elif isinstance(output, boto.ec2.zone.Zone):
            return self.parseEC2Zone(output)
        elif isinstance(output, boto.ec2.address.Address):
            return self.parseAddress(output)
        elif isinstance(output, boto.route53.record.Record):
            return self.parseRecord(output)
        elif isinstance(output, boto.route53.zone.Zone):
            return self.parseR53Zone(output)
        elif isinstance(output, boto.route53.status.Status):
            return self.parseR53Status(output)
        elif isinstance(output, boto.ec2.ec2object.EC2Object):
            return self.parseEC2Object(output)
        #elif isinstance(output, boto.s3.bucket.Bucket):
        #    return self.parseBucket(output)
        else:
            return output

    def formatter(self, output):
        formatted = []
        if isinstance(output, list):
            for o in output:
                formatted.append(self.selector(o))
        else:
            formatted.append(self.selector(output))
        return formatted

    def parseReservation(self, output):
        instance_list = []
        for instance in output.instances:
            instance_data = self.parseInstance(instance)
            instance_data['owner_id'] = output.owner_id
            instance_list.append(instance_data)
        return instance_list

    def parseAddress(self, output):
        instance_data = {field: getattr(output, field) for field in FieldLists.ADDRESS}
        return instance_data

    def parseInstance(self, output):
        instance_data = {field: getattr(output, field) for field in FieldLists.INSTANCE}
        return instance_data

    def parseVolume(self, output):
        volume_data = {field: getattr(output, field) for field in FieldLists.VOLUME}
        return volume_data

    def parseEC2Zone(self, output):
        zone_data = {field: getattr(output, field) for field in FieldLists.EC2ZONE}
        return zone_data

    def parseRecord(self, output):
        record_data = {field: getattr(output, field) for field in FieldLists.RECORD}
        return record_data

    def parseR53Zone(self, output):
        zone_data = {field: getattr(output, field) for field in FieldLists.R53ZONE}
        return zone_data

    def parseR53Status(self, output):
        status_data = {field: getattr(output, field) for field in FieldLists.R53STATUS}
        return status_data

    def parseBucket(self, output):
        bucket_data = {field: getattr(output, field) for field in FieldLists.BUCKET}
        return bucket_data

    def parseEC2Object(self, output):
        # Looks like everything that is an EC2Object pretty much only has these extra
        # 'unparseable' properties so handle region and connection specially.
        output = vars(output)
        del output['connection']
        # special handling for region since name here is better than id.
        region = output.get('region', None)
        output['region'] = region.name if region else ''
        # now anything that is an EC2Object get some special marshalling care.
        for k, v in six.iteritems(output):
            if isinstance(v, boto.ec2.ec2object.EC2Object):
                # Better not to assume each EC2Object has an id. If not found
                # resort to the str of the object which should have something meaningful.
                output[k] = getattr(v, 'id', str(v))
            # Generally unmarshallable object might be hiding in list so better to
            if isinstance(v, list):
                v_list = []
                for item in v:
                    # avoid touching the basic types.
                    if isinstance(item, (basestring, bool, int, long, float)):
                        v_list.append(v)
                    else:
                        v_list.append(str(item))
                output[k] = v_list
        return output
