import json
import requests
from lib.action import PagerDutyAction


class ResolveIncident(PagerDutyAction):
  def run(self, event_key):
    """Resolve an incident"""

    resolve_keys = [x.strip() for x in event_key.split(',')]
#    rs = []
    for arg in resolve_keys:
      self.pager.resolve_incident(self.config['service_api'], arg)
    return resolve_keys

