# pylint: disable=no-member

from items_selector import ItemsSelector
from utils import compact_dict, get_client, chunk_index_list
from easydict import EasyDict
from collections import defaultdict
import curator.api as api
import logging
import sys

logger = logging.getLogger(__name__)


class CuratorInvoke(object):
    # Supported curator commands for indices and snapshots.
    SUPPORTS = {
        'snapshots': ['delete'],
        'indices': [
            'alias', 'allocation', 'bloom', 'close', 'delete',
            'open', 'optimize', 'replicas', 'snapshot'
        ]
    }

    def __init__(self, **opts):
        self.opts = EasyDict(opts)
        self._client = None
        self._iselector = None

    @property
    def client(self):
        if not self._client:
            o = self.opts
            self._client = get_client(**({
                'host': o.host, 'port': o.port, 'url_prefix': o.url_prefix,
                'http_auth': o.http_auth, 'use_ssl': o.use_ssl,
                'master_only': o.master_only, 'timeout': o.timeout
            }))
        return self._client

    @property
    def iselector(self):
        """
        Used to fetch indices/snapshots and apply filter to them.
        """
        if not self._iselector:
            self._iselector = ItemsSelector(self.client, **self.opts)
        return self._iselector

    def _enhanced_working_list(self, command, act_on):
        """Enhance working_list by pruning kibana indices and filtering
        disk space. Returns filter working list.
        :rtype: list
        """
        working_list = self.iselector.fetch(act_on=act_on)

        # Protect against accidental delete
        if command == 'delete':
            logger.info("Pruning Kibana-related indices to prevent accidental deletion.")
            working_list = api.utils.prune_kibana(working_list)

        # If filter by disk space, filter the working_list by space:
        if working_list and command == 'delete':
            if self.opts.disk_space:
                working_list = api.filter.filter_by_space(self.client, working_list,
                                                          disk_space=float(self.opts.disk_space),
                                                          reverse=(self.opts.reverse or True))

        if not working_list:
            logger.error('No %s matched provided args: %s', act_on, self.opts)
            print "ERROR. No {} found in Elasticsearch.".format(act_on)
            sys.exit(99)

        return working_list

    def fetch(self, act_on, on_nofilters_showall=False):
        """
        Forwarder method to indices/snapshots selector.
        """
        return self.iselector.fetch(act_on=act_on, on_nofilters_showall=on_nofilters_showall)

    def command_kwargs(self, command):
        """
        Return kwargs dict for a specific command options or return empty dict.
        """
        opts = defaultdict(lambda: None, self.opts)
        kwargs = {
            'alias': {'alias': opts['name'], 'remove': opts['remove']},
            'allocation': {'rule': opts['rule']},
            'bloom': {'delay': opts['delay']},
            'replicas': {'replicas': opts['count']},
            'optimize': {
                'max_num_segments': opts['max_num_segments'],
                'request_timeout': opts['timeout'],
                'delay': opts['delay']
            },
            'snapshot': {
                'name': opts['name'], 'prefix': opts['snapshot_prefix'],
                'repository': opts['repository'], 'partial': opts['partial'],
                'ignore_unavailable': opts['ignore_unavailable'],
                'include_global_state': opts['include_global_state'],
                'wait_for_completion': opts['wait_for_completion'],
                'request_timeout': opts['timeout']
            }
        }.get(command, {})
        return compact_dict(kwargs)

    def _call_api(self, method, *args, **kwargs):
        """Invoke curator api method call.
        """
        api_method = api.__dict__.get(method)

        logger.debug("Perfoming api call %s with args: %s, kwargs: %s",
                     method, args, kwargs)
        return api_method(self.client, *args, **kwargs)

    def command_on_indices(self, command, working_list):
        """Invoke command which acts on indices and perform an api call.
        """
        kwargs = self.command_kwargs(command)
        method = 'open_indices' if command == 'open' else command

        # List is too big and it will be proceeded in chunks.
        if len(api.utils.to_csv(working_list)) > 3072:
            logger.warn('Very large list of indices.  Breaking it up into smaller chunks.')
            success = True
            for indices in chunk_index_list(working_list):
                if not self._call_api(method, indices, **kwargs):
                    success = False
            return success
        else:
            return self._call_api(method, working_list, **kwargs)

    def command_on_snapshots(self, command, working_list):
        """Invoke command which acts on snapshots and perform an api call.
        """
        if command == 'snapshot':
            method = 'create_snapshot'
            kwargs = self.command_kwargs(command)
            # The snapshot command should get the full (not chunked)
            # list of indices.
            kwargs['indices'] = working_list
            return self._call_api(method, **kwargs)

        elif command == 'delete':
            method = 'delete_snapshot'
            success = True
            for s in working_list:
                if not self._call_api(method, repository=self.opts.repository,
                                      snapshot=s):
                    success = False
            return success
        else:
            # should never get here
            raise RuntimeError("Unexpected method `{}.{}'".format('snapshots', command))

    def invoke(self, command=None, act_on=None):
        """Invoke command through translating it curator api call.
        """
        if command not in self.SUPPORTS[act_on]:
            raise ValueError("Unsupported curator command: {} {}".format(command, act_on))
        if act_on is None:
            raise ValueError("Requires act_on either on `indices' or `snapshots'")

        working_list = self._enhanced_working_list(command, act_on)

        if act_on == 'indices' and command != 'snapshot':
            return self.command_on_indices(command, working_list)
        else:
            # Command on snapshots and snapshot command (which
            # actually has selected indices before).
            return self.command_on_snapshots(command, working_list)
