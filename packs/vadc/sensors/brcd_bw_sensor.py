from st2reactor.sensor.base import PollingSensor
from lib.vadc import Bsd

import json


class brcdBwSensor(PollingSensor):

    def __init__(self, sensor_service, config=None, poll_interval=5):
        super(brcdBwSensor, self).__init__(sensor_service=sensor_service, config=config,
            poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self._stop = False
        self._bw_tracker = None
        self._bsd = None
        self._manage = None
        self._minimum = 10
        self._headroom = 10
        self._roundup = 10
        self._track = 10
        self._warn = 10

    def setup(self):
        self._bsd = Bsd(self._config, self._logger)
        self._bw_tracker = None

    def poll(self):
        self._get_configs()
        bandwidth = self._bsd.getBandwidth()
        bw_tracker = self._get_bw_tracker()
        if self._manage is not None:
            self._manage_bandwidth(bw_tracker, bandwidth)
        else:
            bw_tracker = {}
        self._monitor_bandwidth(bandwidth)
        self._set_bw_tracker(bw_tracker)

    def _get_configs(self):
        self._logger.debug(self._config)
        if "brcd_bw_minimum" in self._config and self._config["brcd_bw_minimum"] is not None:
            self._minimum = int(self._config["brcd_bw_minimum"])
        if "brcd_bw_roundup" in self._config and self._config["brcd_bw_roundup"] is not None:
            self._roundup = int(self._config["brcd_bw_roundup"])
        if "brcd_bw_headroom" in self._config and self._config["brcd_bw_headroom"] is not None:
            self._headroom = int(self._config["brcd_bw_headroom"])
        if "brcd_bw_track" in self._config and self._config["brcd_bw_track"] is not None:
            self._track = int(self._config["brcd_bw_track"])
        if "brcd_bw_warn" in self._config and self._config["brcd_bw_warn"] is not None:
            self._warn = int(self._config["brcd_bw_warn"])
        if "brcd_bw_manage" in self._config and self._config["brcd_bw_manage"] is not None:
            manage = str(self._config["brcd_bw_manage"])
            if manage.lower() == "all":
                self._manage = ["__ALL__"]
            else:
                self._manage = manage.split(',')

    def _manage_bandwidth(self, bw_tracker, bandwidth):
        for instance in bandwidth.keys():
            instData = bandwidth[instance]
            tag = instData["tag"]
            if "__ALL__" in self._manage or instance in self._manage or tag in self._manage:
                tracked = instData["current"]
                tracked += self._roundup - (tracked % self._roundup)
                if tracked < self._minimum:
                    tracked = self._minimum
                if instance not in bw_tracker:
                    bw_tracker[instance] = instData
                    bw_tracker[instance]["tracking"] = []
                while len(bw_tracker[instance]["tracking"]) >= self._track:
                    bw_tracker[instance]["tracking"].pop(0)
                bw_tracker[instance]["tracking"].append(tracked)
                bw_tracker[instance]["current"] = instData["current"]
                bw_tracker[instance]["peak"] = instData["peak"]
                self._issue_update(instance, tracked, instData, bw_tracker, bandwidth)
            else:
                if instance in bw_tracker:
                    bw_tracker.pop(instance)

    def _issue_update(self, instance, tracked, instData, bw_tracker, bandwidth):
            average = sum(bw_tracker[instance]["tracking"]) / len(bw_tracker[instance]["tracking"])
            assign = average if tracked < average else tracked
            assign = int(assign + self._headroom)
            if assign != instData["assigned"]:
                bw_tracker[instance]["assigned"] = assign
                payload = {"action": "update", "instance": instance, "tag": instData["tag"],
                    "bandwidth": assign, "current": instData["current"], "average": average}
                self.sensor_service.dispatch(trigger="vadc.bsd_bandwidth_event", payload=payload)

    def _monitor_bandwidth(self, bandwidth):
        for instance in bandwidth.keys():
            instData = bandwidth[instance]
            tag = instData["tag"]
            if instData["assigned"] - instData["current"] - self._warn <= 0:
                payload = {"action": "alert", "instance": instance, "tag": tag,
                    "bandwidth": instData["assigned"], "current": instData["current"]}
                self.sensor_service.dispatch(trigger="vadc.bsd_bandwidth_event", payload=payload)

    def _get_bw_tracker(self):
        if not self._bw_tracker and hasattr(self._sensor_service, 'get_value'):
            bw_tracker = self._sensor_service.get_value(name='bw_tracker')
            if bw_tracker is not None:
                self._bw_tracker = json.loads(bw_tracker, encoding="utf-8")
            else:
                self._bw_tracker = {}
        return self._bw_tracker

    def _set_bw_tracker(self, bw_tracker):
        self._bw_tracker = bw_tracker

        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name='bw_tracker', value=json.dumps(bw_tracker,
                encoding="utf-8"))

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
