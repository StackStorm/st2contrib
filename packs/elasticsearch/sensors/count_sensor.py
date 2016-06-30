from st2reactor.sensor.base import PollingSensor
from elasticsearch import Elasticsearch
import json

class ElasticsearchCountSensor(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            get_logger() for writing to logs.
            dispatch() for dispatching triggers into the system.
    * self._config
        - contains configuration that was specified as
          config.yaml in the pack.
    * self._poll_interval
        - indicates the interval between two successive poll() calls.
    """

    def setup(self):
        self.host = self._config.get('host', None)
        self.port = self._config.get('port', None)
        self.query_window = "%is" % self._config.get('query_window', None)
        self.query_string = self._config.get('query_string', '{}')
        self.count_threshold = self._config.get('count_threshold', 1)
        self.index = self._config.get('index', '_all')
        self._trigger_ref="elasticsearch.count_event"       
        self.LOG = self.sensor_service.get_logger(__name__)
        self.query = json.loads(self.query_string)
        self.es = None
        
        try:
            self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        except:
            self.LOG.exception("Could not connect to elasticsearch. %s:%i" % (self.host, self.port))
            raise Exception("Could not connect to elasticsearch. %s:%i" % (self.host, self.port))

    def poll(self):
        query_payload={"query": {
                     "bool": {
                         "must": [self.query],
                         "filter": {
                             "range": {
                                 "@timestamp": { "gte": "now-%s" % self.query_window}}}}}}
        data = self.es.search(index=self.index, body=query_payload, size=0)

        hits = data.get('hits', None)
        if hits.get('total', 0) > self.count_threshold:
           payload = {}
           payload['results'] = hits
           payload['results']['query'] = query_payload
           self.LOG.info("Dispatching trigger")
           self.sensor_service.dispatch(trigger=self._trigger_ref, payload=payload)

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
