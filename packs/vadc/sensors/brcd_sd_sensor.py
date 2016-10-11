from st2reactor.sensor.base import PollingSensor
from lib.vadc import Bsd

import json


class brcdSdSensor(PollingSensor):

  def __init__(self, sensor_service, config=None, poll_interval=5):
    super(brcdSdSensor, self).__init__(sensor_service=sensor_service, config=config, poll_interval=poll_interval)
    self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
    self._stop = False
    self._bsd = None


  def setup(self):
    self._bsd = Bsd(self._config, self._logger)
    self._last_errors = None
    pass

  def poll(self):
    try:
      errors = self._bsd.getErrors()
      last_errors = self._get_last_errors()
      self._set_last_errors( errors )
      self._process_changes(errors, last_errors)
      if last_errors and not errors:
        payload = { "errors": "vTM Error ALL CLEAR!" }
        self.sensor_service.dispatch(trigger="vadc.bsd_failure_event", payload=payload)
    except Exception as e:
      payload = { "errors": "BSD Sensor: {}: {}".format(self._config["brcd_sd_host"], e) }
      self.sensor_service.dispatch(trigger="vadc.bsd_failure_event", payload=payload)
    
  def _process_changes(self, errors, last_errors):
    for instance in errors:
      if instance in last_errors:
        if errors[instance] != last_errors[instance]:
          # This has changed
          payload = { "errors":  "vTM Error Updated: " + json.dumps(errors[instance], encoding="utf-8") }
          self.sensor_service.dispatch(trigger="vadc.bsd_failure_event", payload=payload)
      else:
        # New error
        payload = { "errors":  "vTM Error New: " + json.dumps(errors[instance], encoding="utf-8") }
        self.sensor_service.dispatch(trigger="vadc.bsd_failure_event", payload=payload)
    for instance in last_errors:
      if instance not in errors:
        payload = { "errors":  "vTM Error Resolved: " + json.dumps(last_errors[instance], encoding="utf-8") }
        self.sensor_service.dispatch(trigger="vadc.bsd_failure_event", payload=payload)

  def _get_last_errors(self):
    if not self._last_errors and hasattr(self._sensor_service, 'get_value'):
      self._last_errors = json.loads(self._sensor_service.get_value(name='last_errors'), encoding="utf-8")
    return self._last_errors

  def _set_last_errors(self, last_errors):
    self._last_errors = last_errors

    if hasattr(self._sensor_service, 'set_value'):
      self._sensor_service.set_value(name='last_errors', value=json.dumps(last_errors, encoding="utf-8"))


  def cleanup(self):
    # This is called when the st2 system goes down. You can perform cleanup operations like
    # closing the connections to external system here.
    pass

  def add_trigger(self, trigger):
    # This method is called when trigger is created
    pass

  def update_trigger(self, trigger):
    # This method is called when trigger is updated
    pass

  def remove_trigger(self, trigger):
    # This method is called when trigger is deleted
    pass

