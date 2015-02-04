from lib.action import PagerDutyAction


class AckIncident(PagerDutyAction):
  def run(self, event_key):
    """Acknowledgment of a trigger, You can provide a list of keys"""    
#    ack_keys = event_key.split(",")
    ack_keys = [x.strip() for x in event_key.split(',')]
   
    for arg in ack_keys:
      self.pager.acknowledge_incident(self.config['service_api'], arg)
 
    return ack_keys

