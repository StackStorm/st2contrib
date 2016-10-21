#!/usr/bin/env python

__all__ = [
    'ResultSets'
]


FIELD_LIST_MAP = {
    'room': ['id', 'name']
}


class ResultSets(object):

    def selector(self, output):
        try:
            field_list = FIELD_LIST_MAP.get(output.__class__)
            return self.parse(output, field_list)
        except KeyError:
            return output

    def formatter(self, output):
        formatted = []
        if isinstance(output, list):
            for o in output:
                formatted.append(self.selector(o))
        else:
            formatted = self.selector(output)
        return formatted

    def _getval(self, obj, field):
        return self.selector(getattr(obj, field))

    def parse(self, output, field_list):
        instance_data = {field: self._getval(output, field) for field in field_list}
        return instance_data
