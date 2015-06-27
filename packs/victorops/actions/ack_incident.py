import json
import time

import requests

from lib.action import VictorOpsAction


class AckIncident(VictorOpsAction):
    def run(self, entity, message=None):
        prms = {
            "message_type": 'ACKNOWLEDGEMENT',
            "timestamp": int(time.time()),
            "entity_id": entity,
            "state_message": message
        }
        post_data = json.dumps(prms)
        requests.post(self.url, post_data)
        return True
