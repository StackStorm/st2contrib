import requests
from lib.action import VictorOpsAction
import json
import time


class AckIncident(VictorOpsAction):
    def run(self, entity, message=None):
        prms = {
                "message_type": 'RECOVERY',
                "timestamp": int(time.time()),
                "entity_id": entity,
                "state_message": message}
        post_data = json.dumps(prms)
        data = requests.post(self.url, post_data)

