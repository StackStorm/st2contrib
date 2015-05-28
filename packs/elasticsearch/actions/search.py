# pylint: disable=no-member

from easydict import EasyDict
from lib.items_selector import ItemsSelector
from lib.esbase_action import ESBaseAction
import logging
import sys
import elasticsearch
import json

logger = logging.getLogger(__name__)


class SearchRunner(ESBaseAction):

    def __init__(self, config=None):
        super(SearchRunner, self).__init__(config=config)
        self._iselector = None

    @property
    def iselector(self):
        """
        Used to fetch indices/snapshots and apply filter to them.
        """
        if not self._iselector:
            kwargs = self.config.copy()
            # Support iselectors parameters
            kwargs.update({'dry_run': False})
            self._iselector = ItemsSelector(self.client, **kwargs)
        return self._iselector

    def run(self, action=None, log_level='warn', operation_timeout=600, **kwargs):
        kwargs.update({
            'timeout': int(operation_timeout),
            'log_level': log_level
        })
        self.config = EasyDict(kwargs)
        self.set_up_logging()

        if action.endswith('.q'):
            self.simple_search()
        else:
            self.full_search()

    def simple_search(self):
        """Perform URI-based request search.
        """
        accepted_params = ('q', 'df', 'default_operator', 'from', 'size')
        kwargs = {k: self.config[k] for k in accepted_params if self.config[k]}
        indices = ','.join(self.iselector.indices())

        try:
            result = self.client.search(index=indices, **kwargs)
        except elasticsearch.ElasticsearchException as e:
            logger.error(e.message)
            sys.exit(2)

        self._pp_exit(result)

    def full_search(self):
        """Perform search using Query DSL.
        """
        accepted_params = ('from', 'size')
        kwargs = {k: self.config[k] for k in accepted_params if self.config[k]}
        try:
            result = self.client.search(index=self.config.index,
                                        body=self.config.body, **kwargs)
        except elasticsearch.ElasticsearchException as e:
            logger.error(e.message)
            sys.exit(2)

        self._pp_exit(result)

    def _pp_exit(self, data):
        """Print Elastcsearch JSON response and exit.
        """
        kwargs = {}
        if self.config.pretty:
            kwargs = {'indent': 4}
        print json.dumps(data, **kwargs)

        if data['hits']['total'] > 0:
            sys.exit(0)
        else:
            sys.exit(1)
