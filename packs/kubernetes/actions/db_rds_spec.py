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
        instance_class = 'db.m3.xlarge'
        port = '3306'
        rds_engine = 'mysql'
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
        pass

    def _id_generator(self):
        return uuid.uuid4().hex
        pass
