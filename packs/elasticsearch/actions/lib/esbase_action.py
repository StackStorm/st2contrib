# pylint: disable=no-member

from utils import get_client
from st2actions.runners.pythonrunner import Action
import logging


class ESBaseAction(Action):

    def __init__(self, config=None):
        super(ESBaseAction, self).__init__(config=config)
        self._client = None

    @property
    def client(self):
        if not self._client:
            o = self.config
            self._client = get_client(**({
                'host': o.host, 'port': o.port, 'url_prefix': o.url_prefix,
                'http_auth': o.http_auth, 'use_ssl': o.use_ssl,
                'master_only': o.master_only, 'timeout': o.timeout
            }))
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
