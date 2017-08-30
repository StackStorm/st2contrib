import json
import time

import requests

from lib.action import VictorOpsAction


class OpenIncident(VictorOpsAction):
    def run(self, severity, entity, message=None, notify_group=None):
        prms = {
            "message_type": severity,
            "timestamp": int(time.time()),
            "entity_id": entity,
            "state_message": message}
        post_data = json.dumps(prms)
        if notify_group is not None:
            url = self.url.replace(self.url.split("/")[-1], notify_group)
        else:
            url = self.url
        requests.post(url, post_data)
        return True
