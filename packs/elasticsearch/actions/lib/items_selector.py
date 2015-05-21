# pylint: disable=no-member

from curator.api.utils import *  # noqa
from curator.api.filter import *  # noqa
from items_filter import ItemsFilter
from easydict import EasyDict
from utils import xstr
import sys
import logging

logger = logging.getLogger(__name__)


class ItemsSelector(object):

    def __init__(self, client, **opts):
        self.opts = EasyDict(opts)
        self.client = client
        self.ifilter = ItemsFilter().build(**opts)

    def _apply_filters(self, source_items, act_on):
        """Applies filters to a list of indices or snapshots.
        :param source_items:   List of indices or snapshots.
        :param act_on:  Specifies whether we act on indices or snapshots.
        """
        opts = self.opts
        all_items_selected = opts.get('all_{0}'.format(act_on), None)

        # Choose explicitly chosen indices or snapshots
        #
        if act_on == 'indices':
            explicit_items = opts.index or []
        else:
            explicit_items = opts.snapshot or []

        # I don't care about using only timestring if it's a `dry_run` of show
        if not any((xstr(opts.newer_than), xstr(opts.older_than), opts.dry_run)) and \
                opts.timestring:
            logger.warn('Used only timestring parameter.')
            logger.warn('Actions can be performed on all %s matching %s', act_on, opts.timestring)

        logger.debug("Full list of %s: %s", act_on, source_items)

        if not source_items:
            print 'ERROR. No {0} found in Elasticsearch.'.format(act_on)
            sys.exit(1)
        else:
            working_list = source_items

        # No filters has been added and not all items selected,
        # this means index or snapshot parameter is used alone.
        if not all_items_selected and not self.ifilter.filter_list:
            working_list = []
        else:
            # Otherwise safely apply filtering
            working_list = self.ifilter.apply(working_list, act_on=act_on)

        # Include explict items into resulting working list.
        if explicit_items:
            working_list.extend((i for i in explicit_items if i in source_items))

        if not working_list:
            logger.error('No %s matched provided args: %s', act_on, opts)
            print "ERROR. No {} found in Elasticsearch.".format(act_on)
            sys.exit(99)

        # Make a sorted, unique list of indices/snapshots
        return sorted(list(set(working_list)))

    def snapshots(self, on_nofilters_showall=False):
        """
        Get a list of snapshots to act on from the provided arguments.
        """
        if not any((self.opts.all_snapshots, self.opts.snapshot, self.ifilter.filter_list)):
            if on_nofilters_showall:
                self.opts.all_snapshots = True
            else:
                print 'Error: At least one snapshot filter parameter must be provided!'
                sys.exit(1)

        if not self.opts.repository:
            print 'Missing required parameter: repository.'
            sys.exit(1)

        # Get a master-list of snapshots
        snapshots = get_snapshots(self.client, repository=self.opts.repository)
        return self._apply_filters(snapshots, act_on='snapshots')

    def indices(self, on_nofilters_showall=False):
        """
        Get a list of indices to act on from the provided arguments.
        """
        # Check if we have selection to operate
        if not any((self.opts.all_indices, self.opts.index, self.ifilter.filter_list)):
            if on_nofilters_showall:
                self.opts.all_indices = True
            else:
                print 'Error: At least one index filter parameter must be provided!'
                sys.exit(1)

        # Get a master-list of indices
        indices = get_indices(self.client)
        return self._apply_filters(indices, act_on='indices')

    def fetch(self, act_on, on_nofilters_showall=False):
        if act_on not in ['indices', 'snapshots']:
            raise ValueError('invalid argument: %s', act_on)

        if act_on == 'indices':
            return self.indices(on_nofilters_showall=on_nofilters_showall)  # noqa
        else:
            return self.snapshots(on_nofilters_showall=on_nofilters_showall)  # noqa
