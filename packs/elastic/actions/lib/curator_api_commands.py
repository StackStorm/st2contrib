from easydict import EasyDict
from utils import compact_dict
from collections import defaultdict
from items_selector import ItemsSelector
import curator.api as api
import utils
import logging

logger = logging.getLogger(__name__)


CMD_TO_API = {
    'snapshot':         'create_snapshot',
    'open':             'open_indices',
    'delete.indices':   'delete',
    'delete.snapshots': 'delete_snapshot'
}


class APICommands(object):
    SUPPORTS = [ 'alias', 'allocation', 'bloom', 'close', 'open', 'optimize',
                 'replicas', 'snapshot', 'delete.indices', 'delete.snapshots' ]

    def __init__(self, **opts):
        self.opts = EasyDict(opts)
        self._client = None
        self._iselector  = None


    @property
    def client(self):
        if not self._client:
            o = self.opts
            self._client = utils.get_client(**({
                'host': o.host, 'port': o.port, 'url_prefix': o.url_prefix,
                'http_auth': o.http_auth, 'use_ssl': o.use_ssl,
                'master_only': o.master_only, 'timeout': o.operation_timeout
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


    def command_acts_on(self, command):
        if '.snapshots' in command:
            return 'snapshots'
        return 'indices'


    def _chunk_index_list(indices):
        """
        This utility chunks very large index lists into 3KB chunks
        It measures the size as a csv string, then converts back into a list
        for the return value.
        :arg indices: A list of indices to act on.

        !When version > 3.0.3 of curator is released. Should be removed!
        """
        chunks = []
        chunk = ""
        for index in indices:
            if len(chunk) < 3072:
                if not chunk:
                    chunk = index
                else:
                    chunk += "," + index
            else:
                chunks.append(chunk.split(','))
                chunk = index
        chunks.append(chunk.split(','))
        return chunks


    def _enhanced_working_list(self, command):
        """Enhance working_list by pruning kibana indices and filtering
        disk space. Returns filter working list.
        :rtype: list
        """
        act_on = self.command_acts_on(command)
        working_list = self.iselector.fetch(act_on=act_on)

        # Protect against accidental delete
        if command == 'delete':
            logger.info("Pruning Kibana-related indices to prevent accidental deletion.")
            working_list = api.utils.prune_kibana(working_list)

        # If filter by disk space, filter the working_list by space:
        if working_list and command == 'delete':
            if self.opts.disk_space:
                working_list = api.filter.filter_by_space(
                                    client, working_list,
                                    disk_space=float(self.opts.disk_space),
                                    reverse=(self.opts.reverse or True)
                               )
        return working_list


    def fetch(self, act_on, nofilters_showall=False):
        """
        Forwarder method to indices/snapshots selector.
        """
        return self.iselector.fetch(act_on=act_on, nofilters_showall=nofilters_showall)


    def command_kwargs(self, command):
        """
        Return kwargs dict for a specific command options or return empty dict.
        """
        opts = defaultdict(lambda: None, self.opts)
        kwargs = {
            'alias': { 'alias': opts['name'], 'remove': opts['remove'] },
            'allocation': { 'rule': opts['rule'] },
            'bloom': { 'delay': opts['delay'] },
            'replicas': { 'replicas': opts['count'] },
            'optimize': {
                'max_num_segments': opts['max_num_segments'],
                'request_timeout': opts['operation_timeout'],
                'delay': opts['delay']
            },
            'snapshot': {
                'name': opts['name'], 'prefix': opts['snapshot_prefix'],
                'repository': opts['repository'], 'partial': opts['partial'],
                'ignore_unavailable': opts['ignore_unavailable'],
                'include_global_state': opts['include_global_state'],
                'wait_for_completion': opts['wait_for_completion'],
                'request_timeout': opts['operation_timeout']
            }
        }.get(command, {})
        return compact_dict(kwargs)


    def _call_api(self, command, *args, **kwargs):
        """Invoke curator api method call.
        """
        func_name = CMD_TO_API.get(command, command)
        api_method = api.__dict__.get(func_name)
        return api_method(self.client, *args, **kwargs)


    def command_on_indices(self, command, working_list):
        """Invoke command which acts on indices and perform an api call.
        """
        kwargs = self.command_kwargs(command)
        # List is too big and it will be proceeded in chunks.
        if len(api.utils.to_csv(working_list)) > 3072:
            logger.warn('Very large list of indices.  Breaking it up into smaller chunks.')
            success = True
            for indices in chunk_index_list(working_list):
                if not self._call_api(command, *(indices), **kwargs):
                    success = False
            return success
        else:
            return self._call_api(command, *(working_list), **kwargs)


    def command_on_snapshots(self, command, working_list):
        """Invoke command which acts on snapshots and perform an api call.
        """
        if command == 'snapshot':
            kwargs = self.command_kwargs(command)
            # The snapshot command should get the full (not chunked)
            # list of indices.
            kwargs['indices'] = working_list
            return self._call_api(command, **kwargs)

        elif command == 'delete.snapshots':
            success = True
            for s in working_list:
                if not self._call_api(command, repository=self.opts.repository,
                                               snapshot=s):
                    success = False
            return success
        else:
            # should never get here
            raise RuntimeError("Unexpected method `{0}'".format(command))


    def invoke(self, command=None):
        """Invoke command through translating it curator api call.
        """
        if command not in self.SUPPORTS:
            raise ValueError("Unsupported curator API call `{0}'".format(command))

        act_on = self.command_acts_on(command)
        working_list = self._enhanced_working_list(command)

        if act_on == 'indices' and command != 'snapshot':
            return self.command_on_indices(command, working_list)
        else:
            # Command on snapshots and snapshot command (which
            # actually has selected indices before).
            return self.command_on_snapshots(command, working_list)
