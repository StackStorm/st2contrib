from st2actions.runners.pythonrunner import Action
import utils
import logging

class ElasticAction(Action):

    def __init__(self, config=None):
        super(ElasticAction, self).__init__(config=config)
        self._client = None


    @property
    def client(self):
        if not self._client:
            self._client = utils.get_client(**self.config)
        return self._client


    def set_up_logging(self):
        """
        Set log_level. Default is to display warnings.
        """
        log_level = self.config.log_level or 'warn'
        numeric_log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError('Invalid log level: {0}'.format(log_level))
        logging.basicConfig(level=numeric_log_level)
