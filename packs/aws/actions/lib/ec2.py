# pylint: disable=no-member
import logging
import boto.ec2


LOG = logging.getLogger(__name__)


class EC2(object):

    def __init__(self, config):
        self._region = config['region']
        self._access_key_id = config['access_key_id']
        self._secret_access_key = config['secret_access_key']
        self._interval = config['interval']
        self.conn = self.connect(self._region)

    def connect(self, region):
        return boto.ec2.connect_to_region(region,
                                          aws_access_key_id=self._access_key_id,
                                          aws_secret_access_key=self._secret_access_key)

    def get_object(self, action):
        return getattr(boto.ec2.connection.EC2Connection, action)
