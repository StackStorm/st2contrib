import json
import requests
from lib.action import PagerDutyAction


class LaunchIncident(PagerDutyAction):
  def run(self, description, details):
    """lauch a trigger """
    lst = self.pager.trigger_incident(self.config['service_api'], description=description, details=details) 
    return lst
   
