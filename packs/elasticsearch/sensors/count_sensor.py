from st2reactor.sensor.base import PollingSensor
from elasticsearch import Elasticsearch
import json
import eventlet


class ElasticsearchCountSensor(PollingSensor):

    def setup(self):
        self.host = self.config.get('host', None)
        self.port = self.config.get('port', None)
        self.query_window = self.config.get('query_window', 60)
        self.query_string = self.config.get('query_string', '{}')
        self.cooldown_multiplier = self.config.get('cooldown_multiplier', 0)
        self.count_threshold = self.config.get('count_threshold', 0)
        self.index = self.config.get('index', '_all')
        self._trigger_ref = "elasticsearch.count_event"
        self.LOG = self.sensor_service.get_logger(__name__)
        self.query = json.loads(self.query_string)
        self.es = None

        try:
            self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        except Exception:
            raise

    def poll(self):
        query_payload = {"query": {
                         "bool": {
                             "must": [self.query],
                             "filter": {
                                 "range": {
                                     "@timestamp": {
                                         "gte": "now-%ss" %
                                         self.query_window}}}}}}
        data = self.es.search(index=self.index, body=query_payload)

        hits = data.get('hits', None)
        if hits.get('total', 0) > self.count_threshold:
            payload = dict()
            payload['results'] = hits
            payload['results']['query'] = query_payload
            self.LOG.info("Dispatching trigger")
            self.sensor_service.dispatch(trigger=self._trigger_ref,
                                         payload=payload)
            cooldown = (self.query_window * self.cooldown_multiplier)
            self.LOG.info("Cooling down for %i seconds" % cooldown)
            eventlet.sleep(cooldown)

    def cleanup(self):
        # This is called when the st2 system goes down.
        # You can perform cleanup operations like
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
