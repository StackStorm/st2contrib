import boto
import six


class FieldLists():
    ADDRESS = [
        'allocation_id',
        'association_id',
        'domain',
        'instance_id',
        'network_interface_id',
        'network_interface_owner_id',
        'private_ip_address',
        'public_ip'
    ]

    BLOCK_DEVICE_TYPE = [
        'attach_time',
        'delete_on_termination',
        'encrypted',
        'ephemeral_name',
        'iops',
        'size',
        'snapshot_id',
        'status',
        'volume_id',
        'volume_type'
    ]

    BUCKET = [
        'connection',
        'creation_date',
        'LoggingGroup',
        'name'
    ]

    EC2ZONE = [
        'messages',
        'name',
        'region_name',
        'state'
    ]

    INSTANCE = [
        'ami_launch_index',
        'architecture',
        'hypervisor',
        'id',
        'image_id',
        'instance_type',
        'ip_address',
        'kernel',
        'key_name',
        'launch_time',
        'monitored',
        'monitoring_state',
        'placement',
        'placement_group',
        'placement_tenancy',
        'platform',
        'previous_state',
        'previous_state_code',
        'private_dns_name',
        'private_ip_address',
        'public_dns_name',
        'ramdisk',
        'root_device_name',
        'root_device_type',
        'spot_instance_request_id',
        'state',
        'state_code',
        'state_reason',
        'subnet_id',
        'tags',
        'virtualization_type',
        'vpc_id',
    ]

    RECORD = [
        'alias_dns_name',
        'alias_evaluate_target_health',
        'alias_hosted_zone_id',
        'failover',
        'health_check',
        'identifier',
        'name',
        'region',
        'resource_records',
        'ttl',
        'type',
        'weight'
    ]

    R53ZONE = [
        'callerreference',
        'config',
        'id',
        'name',
        'resourcerecordsetcount'
    ]

    R53STATUS = [
        'comment',
        'id',
        'status',
        'submittedat'
    ]

    VOLUME = [
        'create_time',
        'encrypted',
        'id',
        'iops',
        'size',
        'snapshot_id',
        'status',
        'type',
        'zone'
    ]

    TAG = [
        'name',
        'value',
        'res_type',
        'res_id'
    ]


class ResultSets(object):

    def __init__(self):
        self.foo = ''

    def selector(self, output):
        if isinstance(output, boto.ec2.instance.Reservation):
            return self.parseReservation(output)
        elif isinstance(output, boto.ec2.instance.Instance):
            return self.parseInstance(output)
        elif isinstance(output, boto.ec2.volume.Volume):
            return self.parseVolume(output)
        elif isinstance(output, boto.ec2.blockdevicemapping.BlockDeviceType):
            return self.parseBlockDeviceType(output)
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
        elif isinstance(output, boto.ec2.tag.Tag):
            return self.parseTag(output)
        elif isinstance(output, boto.ec2.ec2object.EC2Object):
            return self.parseEC2Object(output)
        else:
            return output

    def formatter(self, output):
        if isinstance(output, list):
            return [self.formatter(item) for item in output]
        elif isinstance(output, dict):
            return {key: self.formatter(value) for key, value in six.iteritems(output)}
        else:
            return self.selector(output)

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

    def parseBlockDeviceType(self, output):
        data = {field: getattr(output, field) for field in FieldLists.BLOCK_DEVICE_TYPE}
        return data

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

    def parseTag(self, output):
        tag_data = {field: getattr(output, field) for field in FieldLists.TAG}
        return tag_data

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
