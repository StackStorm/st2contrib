import re
import uuid

from st2actions.runners.pythonrunner import Action


class DatabaseRdsSpec(Action):
    def run(self, payload):
        # For dbidentifier
        db_name = re.sub('[^0-9a-zA-Z]+', '-', payload['name']) + "-" + payload['namespace']

        # Lets get a username generated
        user_name = self._user_name(uid=payload['uid'])
        # Lets get a password randomly generated
        pw = self._id_generator()

        if payload['labels']['size']:
            instance_class = payload['labels']['size']
        else:
            instance_class = 'db.m3.xlarge'

        if payload['labels']['port']:
            port = payload['labels']['port']
        else:
            port = '3306'

        if payload['labels']['object']:
            rds_engine = payload['labels']['object']
        else:
            rds_engine = 'mysql'

        if payload['labels']['storage']:
            allocated_storage = payload['labels']['storage']
        else:
            allocated_storage = '50'

        payload = {
            'db_name': db_name,
            'user_name': user_name,
            'pw': pw,
            'instance_class': instance_class,
            'port': port,
            'rds_engine': rds_engine,
            'allocated_storage': allocated_storage,
        }

        return payload

    def _user_name(self, uid):
        short_uid = uid[0:7]
        return "db_" + short_uid

    def _id_generator(self):
        return uuid.uuid4().hex
