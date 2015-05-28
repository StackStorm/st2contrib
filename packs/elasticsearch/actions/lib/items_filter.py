# pylint: disable=no-member

from utils import xstr
from curator.api.filter import apply_filter
from easydict import EasyDict
import curator.api as api
import sys
import logging

logger = logging.getLogger(__name__)


class ItemsFilter(object):
    """
    Class implements curator indices/snapshot filtering by name.
    Supported opts: newer_than, older_than, suffix, prefix, regex, timestring.
    """

    def build(self, **opts):
        """
        Build items filter.

        :rtype: ItemsFilter
        """
        self.opts = EasyDict(opts)
        self.built_list = self._build()
        return self

    def get_timebased(self):
        """
        Get timebased specific filters.

        :rtype: tuple(newer_than, older_than)
        """
        result = {}
        for f in self.built_list:
            if f.get('method', None) in ('newer_than', 'older_than'):
                result[f['method']] = f
                if len(result) == 2:
                    break

        return (result.get('newer_than', None), result.get('older_than', None))

    @property
    def all_items(self):
        return self.opts.get('all_{0}'.format(self.act_on), None)

    @property
    def filter_list(self):
        return self.built_list

    @property
    def closed_timerange(self):
        """
        Closed time range specified, newer_than and older_than both present.
        """
        return len(filter(None, self.get_timebased())) == 2

    def apply(self, working_list, act_on):
        """
        Apply filters to a working list of indices/snapshots and
        return resulting list.
        """
        self.act_on = act_on
        result_list = self._apply_closed_timerange(working_list)

        if self.all_items:
            logger.info('Matching all %s. Ignoring parameters other than exclude.', self.act_on)

        # Closed time range couldn't be applied
        if result_list is None:
            result_list = working_list

        # Apply filters one by one (if any) from the list.
        for f in self.built_list:
            is_timebased = f.get('method', None) in ('newer_than', 'older_than')
            # Don't apply timebased filters for a closed time range.
            if self.closed_timerange and is_timebased:
                continue
            # When all items are seleted ignore filters other than exclude
            if self.all_items and 'exclude' not in f:
                continue

            logger.debug('Applying filter: %s', f)
            result_list = apply_filter(result_list, **f)

        return result_list

    def _apply_closed_timerange(self, working_list):
        """
        Apply separated filtering for a closed time range.
        In case filtering is not applied None is returned.
        """
        if self.closed_timerange:
            newer_than, older_than = self.get_timebased()
            if newer_than['value'] < older_than['value']:
                print 'ERROR: Wrong time period newer_than parameter must be > older_than.'
                sys.exit(1)
            if not self.all_items:
                # We don't apply time range filtering in case of all_* options.
                logger.debug('Applying time range filters, result will be intersection\n'
                             'newer_than: %s\nolder_than: %s', newer_than, older_than)
                newer_range = set(apply_filter(working_list, **newer_than))
                older_range = set(apply_filter(working_list, **older_than))
                result_list = list(newer_range & older_range)
                return result_list

    def _build(self):
        """
        Build filter accoriding to filtering parameters.

        :rtype: list
        """
        opts = self.opts
        filter_list = []

        # No timestring parameter, range parameters a given
        if not opts.timestring and any((xstr(opts.newer_than),
                                        xstr(opts.older_than))):
            print 'ERROR: Parameters newer_than/older_than require timestring to be given'
            sys.exit(1)
        # Timestring used alone without newer_than/older_than
        if opts.timestring is not None and not all((xstr(opts.newer_than),
                                                    xstr(opts.older_than))):
            f = api.filter.build_filter(kindOf='timestring',
                                        value=opts.timestring)
            if f:
                filter_list.append(f)

        # Timebase filtering
        timebased = zip(('newer_than', 'older_than'), (opts.newer_than,
                                                       opts.older_than))
        for opt, value in timebased:
            if value is None:
                continue
            f = api.filter.build_filter(kindOf=opt, value=value,
                                        timestring=opts.timestring,
                                        time_unit=opts.time_unit)
            if f:
                filter_list.append(f)

        # Add filtering based on suffix|prefix|regex
        patternbased = zip(('suffix', 'prefix', 'regex'),
                           (opts.suffix, opts.prefix, opts.regex))

        for opt, value in patternbased:
            if value is None:
                continue
            f = api.filter.build_filter(kindOf=opt, value=value)
            if f:
                filter_list.append(f)

        # Add exclude filter
        for pattern in opts.exclude or []:
            f = {'pattern': pattern, 'exclude': True}
            filter_list.append(f)

        return filter_list
